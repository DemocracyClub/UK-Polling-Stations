import glob, os
from importlib.machinery import SourceFileLoader
from django.apps import apps
from django.core.management.base import BaseCommand

from pollingstations.models import PollingStation

"""
Run all of the import scripts relating to a particular election or elections
"""
class Command(BaseCommand):

    """
    Turn off auto system check for all apps
    We will maunally run system checks only for the
    'data_collection' and 'pollingstations' apps
    """
    requires_system_checks = False

    summary = []
    exclude = [
        'import_crowdsourced_csv.py'
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '-e',
            '--elections',
            nargs='+',
            help='<Required> List of one or more election ids to import data for',
            required=True
        )

        parser.add_argument(
            '-o',
            '--overwrite',
            help='<Optional> Force deleting of existing data',
            action='store_true',
            required=False,
            default=False
        )

    def importer_covers_these_elections(self, args_elections, importer_elections):
        for election in args_elections:
            if election in importer_elections:
                return True
        return False

    def output_summary(self):
        for line in self.summary:
            if line[0] == 'INFO':
                self.stdout.write(line[1])
            elif line[0] == 'WARNING':
                self.stdout.write(self.style.ERROR(line[1]))
            else:
                self.stdout.write(line[1])

    def handle(self, *args, **kwargs):
        """
        Manually run system checks for the
        'data_collection' and 'pollingstations' apps
        Management commands can ignore checks that only apply to
        the apps supporting the website part of the project
        """
        self.check([
            apps.get_app_config('data_collection'),
            apps.get_app_config('pollingstations')
        ])

        files = glob.glob(
            os.path.abspath('polling_stations/apps/data_collection/management/commands') + '/import_*.py'
        )
        # loop over all the import scripts
        for f in files:
            head, tail = os.path.split(f)

            if tail in self.exclude:
                continue

            try:
                command = SourceFileLoader("module.name", f).load_module()
            except:
                # usually we want to handle a specific exception, but in in this situation
                # if there is any issue (at all) trying to load the module,
                # we just want to log it and move on to the next script
                self.summary.append(('WARNING', "%s could not be loaded!" % tail))
                continue

            cmd = command.Command()
            if hasattr(cmd, 'elections'):
                if self.importer_covers_these_elections(kwargs['elections'], cmd.elections):
                    # run the import script

                    # Only run if
                    existing_data = PollingStation.objects.filter(
                        council_id=cmd.council_id).exists()
                    if not existing_data or kwargs.get('overwrite'):
                        self.summary.append(
                            ('INFO', "Ran import script %s" % tail))
                        opts = {
                            'noclean': False,
                            'verbosity': 1
                        }
                        cmd.handle(**opts)
            else:
                self.summary.append(('WARNING', "%s does not contain elections property!" % tail))

        self.output_summary()
