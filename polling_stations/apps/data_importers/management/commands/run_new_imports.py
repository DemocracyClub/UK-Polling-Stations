import re
import subprocess
from pathlib import Path

import boto3
import botocore
from django.apps import apps
from django.core.management import BaseCommand, CommandError, call_command


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


def get_last_import_sha_from_ssm():
    ssm_client = boto3.client("ssm")
    response = ssm_client.get_parameter(Name="LAST_IMPORT_SHA")
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

    def run_scripts(self, changed_paths, opts):
        for script in changed_paths:
            script_path = Path(script)
            try:
                call_command(script_path.stem, **opts)
                self.summary.append(
                    (
                        "INFO",
                        f"Ran import script: {script_path.name}",
                    )
                )
            except Exception as e:
                # usually we want to handle a specific exception, but in this situation
                # if there is any issue (at all) trying to run the command,
                # we just want to log it and move on to the next script
                self.summary.append(
                    ("WARNING", f"{script_path.name} could not be run. Due to {e}")
                )
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

    def update_last_import_sha_on_ssm(self, to_sha):
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

    def handle(self, *args, **options):
        self.check(
            [
                apps.get_app_config("data_importers"),
                apps.get_app_config("pollingstations"),
            ]
        )

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
            self.run_scripts(changed_scripts, cmd_opts)
            self.run_misc_fixes()
            self.update_last_import_sha_on_ssm(to_sha)
        elif has_imports and has_application and is_post_deploy:
            self.stdout.write("App has deployed. OK to run import scripts")
            self.run_scripts(changed_scripts, cmd_opts)
            self.run_misc_fixes()
            self.update_last_import_sha_on_ssm(to_sha)
        elif has_imports and has_application and not is_post_deploy:
            raise CommandError("Need to deploy before running import scripts\n")
        elif not has_imports:
            self.stdout.write(
                "No import scripts have changed. So nothing new to import.\n"
            )
            self.update_last_import_sha_on_ssm(to_sha)
        else:
            self.stdout.write("Not running import scripts")

        self.output_summary()
