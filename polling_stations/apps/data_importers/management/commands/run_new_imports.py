import os
import re
import subprocess
from io import StringIO
from pathlib import Path
from typing import Any, Dict

import boto3
import botocore
import sentry_sdk
from core.slack_client import SlackClient
from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand, call_command
from polling_stations.settings.constants.slack import BOTS_TESTING_CHANNEL


def get_paths_changed(from_sha, to_sha):
    args = ["git", "diff", "--name-only", from_sha, to_sha]
    output = subprocess.check_output(args)
    return output.decode().splitlines()


def git_rev_parse(rev):
    return subprocess.check_output(["git", "rev-parse", f"{rev}"]).decode().strip()


def get_changed_scripts(changed):
    if any_import_scripts(changed):
        return [p for p in changed if is_import_script(p)]
    return []


def is_import_script(path):
    if re.search(
        r"polling_stations/apps/data_importers/management/commands/import_(?!eoni).+\.py",
        path,
    ):
        return True
    return False


def any_import_scripts(changed):
    return any(is_import_script(path) for path in changed)


def any_non_import_scripts(changed):
    return any(not is_import_script(path) for path in changed)


def sha_in_tree(sha):
    try:
        git_rev_parse(sha)
        return True
    except subprocess.CalledProcessError:
        return False


class LastImportShaNotInTreeError(Exception):
    pass


def get_last_import_sha_from_ssm():
    ssm_client = boto3.client("ssm")
    response = ssm_client.get_parameter(Name="LAST_IMPORT_SHA")
    last_import_sha = response["Parameter"]["Value"]
    if not sha_in_tree(last_import_sha) and settings.DC_ENVIRONMENT == "development":
        # We often end up with an out of tree sha in parameter store on development.
        # Just set 'from_sha' to master
        return git_rev_parse("master")
    if not sha_in_tree(last_import_sha):
        raise LastImportShaNotInTreeError(
            f"Value of LAST_IMPORT_SHA ('{last_import_sha}') stored in parameter store not in working tree."
        )
    return response["Parameter"]["Value"]


class Command(BaseCommand):
    help = """
        Checks the files changed between two GIT commits
        and decides if import scripts should be run
    """

    # Turn off auto system check for all apps
    # We will manually run system checks only for the
    # 'data_importers' and 'pollingstations' apps
    requires_system_checks = []

    summary = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slack_client = None
        self.messages = []

    @property
    def slack_channel(self):
        return os.environ.get("BOTS_CHANNEL", BOTS_TESTING_CHANNEL)

    def add_arguments(self, parser):
        parser.add_argument(
            "-f",
            "--from-sha",
            help="<Optional> The earliest commit hash against which to search for changed scripts. "
            "Defaults to value of LAST_IMPORT_SHA in ssm parameter store",
        )
        parser.add_argument(
            "-t",
            "--to-sha",
            help="<Optional> The latest commit hash against which to search for changed scripts. Defaults to HEAD",
            default=git_rev_parse("HEAD"),
        )
        parser.add_argument("--post-deploy", action="store_true", default=False)
        parser.add_argument(
            "--slack",
            help="Post a report to slack",
            action="store_true",
        )

    def run_scripts(self, changed_paths, should_post_to_slack, opts):
        for script in changed_paths:
            script_path = Path(script)
            try:
                out = StringIO()
                call_command(script_path.stem, stdout=out, **opts)
                self.summary.append(
                    (
                        "INFO",
                        f"Ran import script: {script_path.name}",
                    )
                )
                self.messages.append(
                    {
                        "header_message": f":pollingstation: *Successfully ran {script_path.stem}*",
                        "detail_message": f"```{out.getvalue()}```",
                    }
                )
            except Exception as e:
                # usually we want to handle a specific exception, but in this situation
                # if there is any issue (at all) trying to run the command,
                # we just want to log it and move on to the next script
                self.summary.append(
                    ("WARNING", f"{script_path.name} could not be run. Due to {e}")
                )
                self.messages.append(
                    {
                        "header_message": f":warning: *Failed to run {script_path.stem}*",
                        "detail_message": f"Error: {str(e)}",
                    }
                )
                sentry_sdk.capture_exception(e)
                continue

    def run_misc_fixes(self):
        call_command("misc_fixes")

    def output_summary(self):
        for line in self.summary:
            if line[0] == "INFO":
                self.stdout.write(line[1])
            elif line[0] == "WARNING":
                self.stdout.write(self.style.ERROR(line[1]))
            else:
                self.stdout.write(line[1])

    def update_last_import_sha_on_ssm(self, to_sha, dc_environment=None):
        self.stdout.write("Updating LAST_IMPORT_SHA on ssm...")
        try:
            ssm_client = boto3.client("ssm")
            ssm_client.put_parameter(
                Name="LAST_IMPORT_SHA", Value=to_sha, Overwrite=True
            )
            self.stdout.write("...updated LAST_IMPORT_SHA.")
            self.summary.append(
                (
                    "INFO",
                    f"Updated LAST_IMPORT_SHA to: {to_sha}",
                )
            )
        except botocore.exceptions.ClientError as e:
            self.stdout.write("...Failed to update LAST_IMPORT_SHA on ssm.")
            self.summary.append(
                (
                    "WARNING",
                    f"LAST_IMPORT_SHA not updated in parameter store, due to:\n{e}",
                )
            )
        except botocore.exceptions.NoCredentialsError as e:
            self.stdout.write("...Failed to update LAST_IMPORT_SHA on ssm.")
            self.summary.append(
                (
                    "WARNING",
                    f"LAST_IMPORT_SHA not updated in parameter store, due to:\n{e}",
                )
            )

    def post_to_slack(self, header_message: str, detail_message: str = None) -> None:
        try:
            response = self.post_header(header_message)
            if detail_message:
                thread_ts = response.get("ts")
                self.post_details(thread_ts, detail_message)
        except Exception as e:
            self.stderr.write(f"Error posting to Slack: {str(e)}")
            sentry_sdk.capture_exception(e)

    def post_header(self, message: str) -> Dict[str, Any]:
        return self.slack_client.send_message(
            message=message,
        )

    def post_details(self, thread_ts: str, detail_message: str) -> None:
        self.slack_client.send_message(
            message=detail_message,
            thread_ts=thread_ts,
        )

    def handle(self, *args, **options):
        self.check(
            [
                apps.get_app_config("data_importers"),
                apps.get_app_config("pollingstations"),
            ]
        )
        should_post_to_slack = False

        if options.get("slack"):
            self.slack_client = SlackClient(channel=self.slack_channel)
            should_post_to_slack = True

        if not (from_sha := options.get("from_sha")):
            from_sha = get_last_import_sha_from_ssm()

        to_sha = options.get("to_sha")
        is_post_deploy = options.get("post_deploy")

        changed_paths = get_paths_changed(from_sha, to_sha)

        changed_scripts = get_changed_scripts(changed_paths)
        has_imports = any_import_scripts(changed_paths)
        has_application = any_non_import_scripts(changed_paths)

        cmd_opts = {
            "nochecks": True,
            "verbosity": 1,
            "use_postcode_centroids": False,
            "include_past_elections": False,
        }

        self.stdout.write(
            f"Comparing repo between {from_sha} and {to_sha}\n"
            f"\tFrom: https://github.com/DemocracyClub/UK-Polling-Stations/commit/{git_rev_parse(from_sha)}\n"
            f"\tTo: https://github.com/DemocracyClub/UK-Polling-Stations/commit/{git_rev_parse(to_sha)}\n"
        )

        if has_imports and not has_application:
            self.stdout.write("Only import scripts have changed\n")
            self.stdout.write("Running import scripts\n")
            self.run_scripts(changed_scripts, should_post_to_slack, cmd_opts)
            self.run_misc_fixes()
            self.update_last_import_sha_on_ssm(to_sha)
        elif has_imports and has_application and is_post_deploy:
            self.stdout.write("App has deployed. OK to run import scripts")
            self.run_scripts(changed_scripts, should_post_to_slack, cmd_opts)
            self.run_misc_fixes()
            self.update_last_import_sha_on_ssm(to_sha)
        elif has_imports and has_application and not is_post_deploy:
            self.stdout.write("Need to deploy before running import scripts\n")
        elif not has_imports:
            self.stdout.write(
                "No import scripts have changed. So nothing new to import.\n"
            )
            self.update_last_import_sha_on_ssm(to_sha)
        else:
            self.stdout.write("Not running import scripts")

        self.output_summary()

        if should_post_to_slack:
            for message in self.messages:
                self.post_to_slack(**message)
