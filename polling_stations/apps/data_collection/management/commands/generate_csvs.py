"""
Generate CSV templates for collecting
crowd sourced polling station data
"""

import csv, glob, os
from django.core.management.base import BaseCommand
from pollingstations.models import PollingDistrict
from .import_england_districts import EXCLUSIONS, BAD_DATA

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'output_path',
            help="""Path to export CSVs to e.g:
            '/home/user/ukpollingstations/UK-Polling-Stations/data/crowdsourcing/ref.2016-06-23/'
            (must be an empty dir)
            """
        )

    def generate_files(self):
        # grab councils we want to build a csv for
        # exclude records relating to:
        # the councils we already have and
        # councils with data quality issues
        councils = PollingDistrict.objects\
            .exclude(council__in = self.exclusions)\
            .exclude(council__in = self.bad_data)\
            .distinct("council")\
            .order_by("council")

        for council in councils:
            self.generate_file(council.council_id)

        self.stdout.write("wrote %s files" % (councils.count()))

    def generate_file(self, council_id):
        districts = PollingDistrict.objects.filter(
            council=council_id
        ).order_by("internal_council_id")

        self.stdout.write('writing: ' + "%s.csv" % (council_id))

        with open(os.path.abspath("%s/%s.csv" % (self.output_path, council_id)), 'w') as csvfile:
            fieldnames = ['council_name', 'council_code', 'polling_district_id', 'address', 'postcode', 'source']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for district in districts:
                writer.writerow({
                    'council_name': district.council,
                    'council_code': district.council_id,
                    'polling_district_id': district.internal_council_id,
                    'address': '',
                    'postcode': '',
                    'source': ''
                })

    def handle(self, *args, **kwargs):
        self.exclusions = EXCLUSIONS
        self.bad_data = BAD_DATA
        self.output_path = kwargs['output_path']

        existing_files = glob.glob(
            os.path.abspath("%s/" % (self.output_path)) + '/*'
        )
        if existing_files:
            self.stdout.write(self.style.ERROR('Export dir must be empty!'))
            quit()

        self.stdout.write("writing files to: " + os.path.abspath("%s/" % (self.output_path)))
        self.generate_files()
