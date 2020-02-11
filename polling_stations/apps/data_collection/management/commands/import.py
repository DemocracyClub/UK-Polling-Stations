import glob, os, re, traceback
from importlib.machinery import SourceFileLoader
from multiprocessing import Pool
from django import db
from django.apps import apps
from django.core.management.base import BaseCommand

from pollingstations.models import PollingStation


# does this regular expression match any of the elements in this list?
def match_in(regex, lst):
    for el in lst:
        if re.match(regex, el):
            return True
    return False


# load a django management command from file f
def load_command(f):
    command = SourceFileLoader("module.name", f).load_module()
    return command.Command()


# run a django management command from file f
def run_cmd(f, opts):
    cmd = load_command(f)
    try:
        cmd.handle(**opts)
    except Exception as e:
        traceback.print_exc()
        raise e


"""
Run all of the import scripts relating to a particular election or elections

Election id may be either a string or regex. For example:
python manage.py import -e local.buckinghamshire.2017-05-04
python manage.py import -r -e 'local.[a-z]+.2017-05-04'
"""


class Command(BaseCommand):

    """
    Turn off auto system check for all apps
    We will maunally run system checks only for the
    'data_collection' and 'pollingstations' apps
    """

    requires_system_checks = False

    summary = []

    def add_arguments(self, parser):
        parser.add_argument(
            "-e",
            "--elections",
            nargs="+",
            help="<Required> List of one or more election ids to import data for",
            required=True,
        )

        parser.add_argument(
            "-r",
            "--regex",
            help="<Optional> Election ids should be matched as regular expressions",
            action="store_true",
            required=False,
            default=False,
        )

        parser.add_argument(
            "-o",
            "--overwrite",
            help="<Optional> Force deleting of existing data",
            action="store_true",
            required=False,
            default=False,
        )

        parser.add_argument(
            "-m",
            "--multiprocessing",
            help="<Optional> Use multiprocessing for import",
            action="store_true",
            required=False,
            default=False,
        )

    def importer_covers_these_elections(
        self, args_elections, importer_elections, regex
    ):
        for election in args_elections:
            if regex:
                if match_in(election, importer_elections):
                    return True
            else:
                if election in importer_elections:
                    return True
        return False

    def output_summary(self):
        for line in self.summary:
            if line[0] == "INFO":
                self.stdout.write(line[1])
            elif line[0] == "WARNING":
                self.stdout.write(self.style.ERROR(line[1]))
            else:
                self.stdout.write(line[1])

    def run_commands_in_series(self, commands):
        for f, opts in commands:
            run_cmd(f, opts)

    def run_commands_in_parallel(self, commands):
        pool = Pool()
        pool.starmap_async(run_cmd, commands)
        pool.close()
        pool.join()

    def handle(self, *args, **kwargs):
        """
        Manually run system checks for the
        'data_collection' and 'pollingstations' apps
        Management commands can ignore checks that only apply to
        the apps supporting the website part of the project
        """
        self.check(
            [
                apps.get_app_config("data_collection"),
                apps.get_app_config("pollingstations"),
            ]
        )

        base_path = os.path.dirname(__file__)
        files = glob.glob(base_path + "/import_*.py")

        if not files:
            raise ValueError("No importers matched")

        commands_series = []
        commands_parallel = []
        opts = {
            "noclean": False,
            "nochecks": True,
            "verbosity": 1,
            "use_postcode_centroids": False,
        }
        if kwargs["multiprocessing"]:
            opts = {
                "noclean": False,
                "nochecks": True,
                "verbosity": 0,
                "use_postcode_centroids": False,
            }

        # loop over all the import scripts
        # and build up a list of management commands to run
        for f in files:
            head, tail = os.path.split(f)
            try:
                cmd = load_command(f)
            except:
                # usually we want to handle a specific exception, but in in this situation
                # if there is any issue (at all) trying to load the module,
                # we just want to log it and move on to the next script
                self.summary.append(("WARNING", "%s could not be loaded!" % tail))
                continue

            if hasattr(cmd, "elections"):
                if self.importer_covers_these_elections(
                    kwargs["elections"], cmd.elections, kwargs["regex"]
                ):
                    # Only run if
                    existing_data = PollingStation.objects.filter(
                        council_id=cmd.council_id
                    ).exists()
                    if not existing_data or kwargs.get("overwrite"):
                        self.summary.append(
                            ("INFO", f"Ran import script for {cmd.council_id}: {tail}")
                        )
                        if hasattr(cmd, "run_in_series"):
                            commands_series.append((f, opts))
                        else:
                            commands_parallel.append((f, opts))
            else:
                self.summary.append(
                    ("WARNING", "%s does not contain elections property!" % tail)
                )

        print(
            "running %i import scripts..."
            % (len(commands_series) + len(commands_parallel))
        )
        # run all the import scripts
        if kwargs["multiprocessing"]:
            # do anything we want to run in series first
            self.run_commands_in_series(commands_series)

            # before kicking off parallel imports, close any open
            # DB connections. Otherwise, Django will throw
            # django.db.utils.DatabaseError: lost synchronization with server
            db.connections.close_all()
            self.run_commands_in_parallel(commands_parallel)
        else:
            self.run_commands_in_series(commands_parallel + commands_series)

        self.output_summary()
