from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000126'
    addresses_name  = 'Properties.csv'
    stations_name   = 'Polling Stations.csv'
    elections       = [
        'local.lancashire.2017-05-04',
        'parl.2017-06-08'
    ]

    # South Ribble use Halarose, but they've split the standard export up into
    # 2 files and removed some columns. They've also added grid refs for the
    # stations :) We need to customise a bit..

    station_address_fields = [
        'pollingstationname',
        'pollingstationaddress_1',
        'pollingstationaddress_2',
        'pollingstationaddress_3',
        'pollingstationaddress_4',
    ]

    def get_station_hash(self, record):
        return record.pollingstationnumber.strip()

    def get_station_point(self, record):
        return Point(
            float(record.easting),
            float(record.northing),
            srid=27700
        )

    def get_residential_address(self, record):

        def replace_na(text):
            if text.strip() == 'n/a':
                return ''
            return text.strip()

        address_line_1 = replace_na(record.housenumber)
        street_address = replace_na(record.streetname)
        address_line_1 = address_line_1 + ' ' + street_address

        address = "\n".join([
            address_line_1.strip(),
            replace_na(record.locality),
            replace_na(record.town),
            replace_na(record.adminarea),
        ])

        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()

        return address
