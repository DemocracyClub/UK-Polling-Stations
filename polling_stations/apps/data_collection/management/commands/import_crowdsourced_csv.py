"""
Import crowd sourced polling
station data from CSV file

example usage:
./manage.py import_crowdsourced_csv X01000001 /home/user/ukpollingstations/UK-Polling-Stations/data/crowdsourcing/ref.2016-06-23/X01000001.csv
./manage.py import_crowdsourced_csv X01000001 /home/user/ukpollingstations/UK-Polling-Stations/data/crowdsourcing/pilot/X01000001.csv -c 'latin-1'
"""

import os
from time import sleep
from django.contrib.gis.geos import Point
from councils.models import Council
from data_collection.management.commands import BaseImporter
from data_finder.helpers import geocode, PostcodeError
from pollingstations.models import PollingStation

class Command(BaseImporter):

    csv_encoding = 'utf-8'

    def add_arguments(self, parser):
        parser.add_argument(
            'council_id',
            help='Council ID to report on in the format X01000001'
        )
        parser.add_argument(
            'input_file',
            help="""Path to CSV file to import e.g:
            '/home/user/ukpollingstations/UK-Polling-Stations/data/crowdsourcing/ref.2016-06-23/X01000001.csv'
            """
        )
        parser.add_argument(
            '-c',
            '--character-encoding',
            help='<Optional> Character encoding of the CSV',
            required=False
        )

    def station_record_to_dict(self, record):

        postcode = record.postcode.strip()
        address = record.address.strip()

        if not address and not postcode:
            return None

        # if we have a postcode, attempt to attach a grid ref
        # so we can show the user a map and provide directions
        if postcode:
            sleep(1.3) # ensure we don't hit mapit's usage limit
            try:
                gridref = geocode(postcode)
                location = Point(gridref['wgs84_lon'], gridref['wgs84_lat'], srid=4326)
            except PostcodeError:
                location = None
        else:
            location = None

        return {
            'internal_council_id': record.polling_district_id.strip(),
            'postcode'           : postcode,
            'address'            : address,
            'polling_district_id': record.polling_district_id.strip(),
            'location'           : location
        }

    def handle(self, *args, **kwargs):

        if not os.path.exists(os.path.abspath(kwargs['input_file'])):
            self.stdout.write(self.style.ERROR('Input file does not exist'))
            quit()

        self.council_id = kwargs['council_id']
        head, tail = os.path.split(os.path.abspath(kwargs['input_file']))
        self.base_folder_path = head
        self.stations_name = tail
        if kwargs['character_encoding']:
            self.csv_encoding = kwargs['character_encoding']

        self.council = Council.objects.get(pk=self.council_id)

        # Delete old data for this council
        PollingStation.objects.filter(council=self.council).delete()

        self.import_polling_stations()

        # save and output data quality report
        self.report()
