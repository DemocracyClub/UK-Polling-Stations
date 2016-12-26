"""
Import crowd sourced polling
station data from CSV file or URL

example usage:
./manage.py import_crowdsourced_csv X01000001 -f data/crowdsourcing/ref.2016-06-23/X01000001.csv
./manage.py import_crowdsourced_csv X01000001 -f data/crowdsourcing/pilot/X01000001.csv -c 'latin-1'
./manage.py import_crowdsourced_csv X01000001 -u 'https://docs.google.com/spreadsheet/ccc?key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&output=csv'
"""

import logging
import os
import tempfile
import urllib.request
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode_point_only, PostcodeError
from pollingstations.models import ElectoralRoll


class Command(BaseCsvStationsCsvAddressesImporter):

    addresses_name = None
    stations_name = None
    local_files = False
    csv_encoding = 'utf-8'
    csv_delimiter = ','
    elections = []
    split_districts = set()

    # Additional command line args applicable to import_crowdsourced_csv
    def add_arguments(self, parser):
        parser.add_argument(
            'council_id',
            help='Council ID to import in the format X01000001'
        )
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '-f',
            '--file',
            nargs=1,
            help="""Path to CSV file to import e.g:
            '/home/user/data/elections.2017-05-04/X01000001.csv'
            """
        )
        group.add_argument(
            '-u',
            '--url',
            nargs=1,
            help="""URL to CSV file to import e.g:
            'https://docs.google.com/spreadsheet/ccc?key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&output=csv'
            """
        )
        parser.add_argument(
            '-c',
            '--character-encoding',
            help='<Optional> Character encoding of the CSV',
            required=False
        )

    def get_addresses(self):
        """
        Instead of fetching addresses to import from a CSV file,
        fetch them from the ElectoralRoll table instead
        """
        return ElectoralRoll.objects.filter(council=self.council_id)

    def address_record_to_dict(self, record):
        return {
            'address': record.address,
            'postcode': record.postcode,
            'polling_station_id': record.polling_district_id,
        }

    def get_data_from_file(self, filename):
        if not os.path.exists(os.path.abspath(filename)):
            raise OSError('Input file does not exist')
        return self.get_data(self.stations_filetype, os.path.abspath(filename))

    def get_data_from_url(self, url):
        with tempfile.NamedTemporaryFile() as tmp:
            urllib.request.urlretrieve(url, tmp.name)
            return self.get_data(self.stations_filetype, tmp.name)

    def get_stations(self):
        # stations may be imported from either a local file
        # or straight from a URL (e.g: google docs)

        if 'file' in self.kwargs and self.kwargs['file'] is not None:
            # import from local file system
            return self.get_data_from_file(self.kwargs['file'][0])

        if 'url' in self.kwargs and self.kwargs['url'] is not None:
            # import straight from a url
            return self.get_data_from_url(self.kwargs['url'][0])

    def station_record_to_dict(self, record):

        postcode = record.postcode.strip()
        address = record.address.strip()
        id = record.polling_district_id.strip()

        if id in self.split_districts:
            self.logger.log_message(
                logging.WARNING,
                "found split district - discarding polling station: %s" %\
                (str(id)),
            )
            return None

        if not address and not postcode:
            self.logger.log_message(
                logging.WARNING,
                "found blank row - discarding polling station: %s" % (str(id)),
            )
            return None

        # if we have a postcode, attempt to attach a grid ref
        # so we can show the user a map and provide directions
        if postcode:
            try:
                gridref = geocode_point_only(postcode)
                location = Point(
                    gridref['wgs84_lon'], gridref['wgs84_lat'], srid=4326)
            except PostcodeError:
                location = None
        else:
            location = None

        return {
            'internal_council_id': id,
            'postcode': postcode,
            'address': address,
            'location': location
        }

    # setup tasks for this import script
    def pre_import(self):
        # set character_encoding from command line arg
        if self.kwargs['character_encoding']:
            self.csv_encoding = self.kwargs['character_encoding']

        self.find_split_districts()

    def find_split_districts(self):
        """
        Identify any district codes which appear more than once
        with 2 different polling station addresses.
        We do not want to import these.

        This will make @symroe and @andylolz happy because
        the CSVs can be faithful transcriptions of the CSVs
        and the import script will deal with it gracefully :D
        """
        stations = self.get_stations()
        seen = set()
        for station in stations:
            id = station.polling_district_id.strip()
            if id in seen:
                self.split_districts.add(id)
            seen.add(id)
