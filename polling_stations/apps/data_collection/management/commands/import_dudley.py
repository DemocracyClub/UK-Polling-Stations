from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id      = 'E08000027'
    addresses_name  = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Dudley.tsv'
    stations_name   = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Dudley.tsv'
    elections       = ['local.2018-05-03']
    csv_delimiter   = '\t'
    csv_encoding    = 'windows-1252'

    def station_record_to_dict(self, record):

        if record.polling_place_id == '18095':
            record = record._replace(polling_place_postcode='DY3 3AB')

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.addressline6.strip() == 'B63 4BN':
            return None
        if record.addressline6.strip() == 'B62 9EN':
            return None
        if record.addressline6.strip() == 'DY5 2HN':
            return None
        if record.addressline6.strip() == 'DY6 7JS':
            return None

        return super().address_record_to_dict(record)
