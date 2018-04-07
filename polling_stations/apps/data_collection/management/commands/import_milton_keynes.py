from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E06000042'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def station_record_to_dict(self, record):
        if record.polling_place_id == '5280':
            record = record._replace(polling_place_postcode='MK3 5NG')
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.addressline6.strip() == 'MK18 1AT':
            return None

        if record.addressline6.strip() == 'MK10 7JD':
            return None

        return super().address_record_to_dict(record)
