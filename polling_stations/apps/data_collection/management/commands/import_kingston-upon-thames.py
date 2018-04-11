from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseDemocracyCountsCsvImporter

class Command(BaseDemocracyCountsCsvImporter):
    council_id = 'E09000021'
    addresses_name = 'local.2018-05-03/Version 2/Democracy Club - Polling Districts Kingston.csv'
    stations_name = 'local.2018-05-03/Version 2/Democracy Club - Polling Stations Kingston.csv'
    elections = ['local.2018-05-03']

    def address_record_to_dict(self, record):

        if record.postcode == 'KT1 3JU':
            return None
        if record.postcode == 'KT1 1HG':
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        rec = super().station_record_to_dict(record)

        if rec['internal_council_id'] in ['T_71', 'T_72']:
            rec['location'] = Point(-0.3009045, 51.4146479, srid=4326)

        return rec
