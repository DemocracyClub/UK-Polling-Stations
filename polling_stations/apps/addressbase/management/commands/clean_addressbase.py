import csv
import os
import glob

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Turn off auto system check for all apps
    We will maunally run system checks only for the
    'addressbase' and 'pollingstations' apps
    """
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            'ab_path',
            help='The path to the folder containing the AddressBase CSVs'
        )


    def handle(self, *args, **kwargs):
        """
        Manually run system checks for the
        'addressbase' and 'pollingstations' apps
        Management commands can ignore checks that only apply to
        the apps supporting the website part of the project
        """
        self.check([
            apps.get_app_config('addressbase'),
            apps.get_app_config('pollingstations')
        ])

        self.fieldnames = [
            'UPRN',
            'OS_ADDRESS_TOID',
            'UDPRN',
            'ORGANISATION_NAME',
            'DEPARTMENT_NAME',
            'PO_BOX_NUMBER',
            'SUB_BUILDING_NAME',
            'BUILDING_NAME',
            'BUILDING_NUMBER',
            'DEPENDENT_THOROUGHFARE',
            'THOROUGHFARE',
            'POST_TOWN',
            'DOUBLE_DEPENDENT_LOCALITY',
            'DEPENDENT_LOCALITY',
            'POSTCODE',
            'POSTCODE_TYPE',
            'X_COORDINATE',
            'Y_COORDINATE',
            'LATITUDE',
            'LONGITUDE',
            'RPC',
            'COUNTRY',
            'CHANGE_TYPE',
            'LA_START_DATE',
            'RM_START_DATE',
            'LAST_UPDATE_DATE',
            'CLASS',
        ]
        self.base_path = os.path.abspath(kwargs['ab_path'])
        out_path = os.path.join(self.base_path, 'addressbase_cleaned.csv')

        with open(out_path, 'w') as out_file:
            for csv_path in glob.glob(os.path.join(self.base_path, '*.csv')):
                if csv_path.endswith('cleaned.csv'):
                    continue
                self.out_csv = csv.DictWriter(out_file, fieldnames=[
                    'UPRN',
                    'address',
                    'postcode',
                    'location',
                ])
                print(csv_path)
                self.clean_csv(csv_path)
                out_file.flush()

    def line_filer(self, csv_path):
        with open(csv_path) as csv_file:
            for line in csv.DictReader(csv_file, fieldnames=self.fieldnames):
                # Do any filtering we might need to do here
                yield line

    def clean_csv(self, csv_path):
        for line in self.line_filer(csv_path):
            self.out_csv.writerow(self.clean_output_line(line))

    def clean_address(self, line):
        address_fields = [
            line['ORGANISATION_NAME'],
            line['DEPARTMENT_NAME'],
            line['PO_BOX_NUMBER'],
            line['SUB_BUILDING_NAME'],
            line['BUILDING_NAME'],
            line['BUILDING_NUMBER'],
            line['DEPENDENT_THOROUGHFARE'],
            line['THOROUGHFARE'],
            line['DOUBLE_DEPENDENT_LOCALITY'],
            line['DEPENDENT_LOCALITY'],
            line['POST_TOWN'],
        ]
        return ", ".join([f for f in address_fields if f])

    def clean_output_line(self, line):
        data = {}
        data['UPRN'] = line['UPRN']
        data['address'] = self.clean_address(line)
        data['postcode'] = line['POSTCODE']
        data['location'] = "SRID=4326;POINT({} {})".format(
            line['LONGITUDE'],
            line['LATITUDE'],
        )
        return data
