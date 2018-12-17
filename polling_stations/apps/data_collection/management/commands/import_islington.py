from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000019'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):
        if record.addressline6 == 'N7 9RE':
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if rec['internal_council_id'] == '1404':
            rec['location'] = Point(-0.104049, 51.560139, srid=4326)

        if rec['internal_council_id'] == '1401':
            rec['address'] = "St Joan of Arc Community Centre\nKelross Road\nLondon"
            rec['postcode'] = "N5 2QN"

        return rec
