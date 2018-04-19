from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000086'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Eastleigh.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Eastleigh.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '100060324905':
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.polling_place_uprn == '100062644887':
            record = record._replace(polling_place_postcode='SO53 2FT')

        rec = super().station_record_to_dict(record)
        if record.polling_place_uprn == '10009592012':
            rec['location'] = Point(-1.3198333, 50.8591061, srid=4326)

        return rec
