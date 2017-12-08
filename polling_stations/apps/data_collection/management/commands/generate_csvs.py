"""
Generate CSV templates for collecting
crowd sourced polling station data
"""

import csv, glob, os
from django.core.management.base import BaseCommand
from pollingstations.models import ElectoralRoll


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'output_path',
            help="""Path to export CSVs to e.g:
            '/home/user/data/elections.2017-05-04/'
            (must be an empty dir)
            """
        )

    def generate_files(self):
        # grab councils we want to build a csv for
        councils = ElectoralRoll.objects\
            .distinct("council")\
            .order_by("council")

        for council in councils:
            self.generate_file(council.council_id)

        self.stdout.write("wrote %s files" % (councils.count()))

    def generate_file(self, council_id):
        districts = ElectoralRoll.objects\
            .filter(council=council_id)\
            .distinct("polling_district_id")\
            .order_by("polling_district_id")

        self.stdout.write('writing: ' + "%s.csv" % (council_id))

        filename = os.path.abspath("%s/%s.csv" % (self.output_path, council_id))
        with open(filename, 'w') as csvfile:
            fieldnames = [
                'council_name', 'council_code', 'polling_district_id',
                'address', 'postcode', 'source'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for district in districts:
                writer.writerow({
                    'council_name': district.council,
                    'council_code': district.council_id,
                    'polling_district_id': district.polling_district_id,
                    'address': '',
                    'postcode': '',
                    'source': ''
                })

    def handle(self, *args, **kwargs):
        self.output_path = kwargs['output_path']

        existing_files = glob.glob(
            os.path.abspath("%s/" % (self.output_path)) + '/*'
        )
        if existing_files:
            # dir exists but is not empty
            raise OSError('Export dir must be empty!')

        # if the dir doesn't already exist, create it
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        self.stdout.write(
            "writing files to: " + os.path.abspath("%s/" % (self.output_path)))
        self.generate_files()
