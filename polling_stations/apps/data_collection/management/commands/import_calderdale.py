from django.db import transaction
from django.db import connection
from data_collection.data_types import StationSet
from pollingstations.models import PollingDistrict
from data_collection.management.commands import BaseShpStationsShpDistrictsImporter


class Command(BaseShpStationsShpDistrictsImporter):
    council_id        = 'E08000033'
    districts_name    = 'local.2018-05-03/Version 1/POLLING_DISTRICTS_region.shp'
    stations_name     = 'local.2018-05-03/Version 1/POLLING_STATIONS_region.shp'
    elections         = ['local.2018-05-03']
    station_addresses = {}

    def parse_string(self, text):
        try:
            return text.strip().decode('utf-8')
        except AttributeError:
            return text.strip()

    def district_record_to_dict(self, record):
        code = self.parse_string(record[0])
        name = self.parse_string(record[1])
        address = self.parse_string(record[5])

        """
        Some of the districts don't have a corresponding station point
        in the stations file but every district has a station address.
        We can use these to fill the gaps in later.
        """
        self.station_addresses[code] = address
        return {
            'internal_council_id': code,
            'name': name,
            'polling_station_id': code,
        }

    def station_record_to_dict(self, record):
        code = self.parse_string(record[1])
        address = self.parse_string(record[0])

        if code == '' and address == '':
            return None

        # remove station addresses from the districts file
        # as we find them in the stations file
        if code in self.station_addresses:
            del(self.station_addresses[code])

        return {
            'internal_council_id': code,
            'address': address,
            'postcode': '',
        }

    @transaction.atomic
    def fix_bad_polygon(self):
        # fix self-intersecting polygon
        self.stdout.write("running fixup SQL")
        table_name = PollingDistrict()._meta.db_table

        cursor = connection.cursor()
        cursor.execute("""
        UPDATE {0}
         SET area=ST_Multi(ST_CollectionExtract(ST_MakeValid(area), 3))
         WHERE NOT ST_IsValid(area);
        """.format(table_name))

    @transaction.atomic
    def fill_the_blanks(self):
        # mop up any districts where we have a station address
        # attached to a district code but no point
        self.stations = StationSet()
        for code in self.station_addresses:
            self.add_polling_station({
                'internal_council_id': code,
                'postcode': '',
                'address': self.station_addresses[code],
                'location': None,
                'council': self.council
            })
        self.stations.save()

    def post_import(self):
        self.fill_the_blanks()
        self.fix_bad_polygon()
