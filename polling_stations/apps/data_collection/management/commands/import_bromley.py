from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000006'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (1).tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (1).tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'
    csv_encoding = 'windows-1252'

    def station_record_to_dict(self, record):

        if record.polling_place_id == '8547':
            record = record._replace(polling_place_easting='537322')
            record = record._replace(polling_place_northing='170426')

        if record.polling_place_id == '8694':
            record = record._replace(polling_place_easting='542751')
            record = record._replace(polling_place_northing='172102')

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip('0')

        if record.addressline6 == 'BR7 6HL':
            return None

        return super().address_record_to_dict(record)
