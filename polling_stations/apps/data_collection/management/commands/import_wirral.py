from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E08000015'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'
    csv_encoding = 'windows-1252'

    def station_record_to_dict(self, record):

        if record.polling_place_id == '4115':
            rec = super().station_record_to_dict(record)
            rec['location'] = Point(-3.050648, 53.417306, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.addressline6.strip() == 'CH47 2AZ':
            return None
        if record.addressline6.strip() == 'CH41 8AU':
            return None

        return super().address_record_to_dict(record)
