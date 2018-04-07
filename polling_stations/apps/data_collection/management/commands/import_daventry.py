from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000151'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (1) Daventry.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (1) Daventry.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'
    csv_encoding = 'windows-1252'

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '28052804':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NN6 8HN'
            return rec

        if record.addressline6 == 'NN6 6JQ':
            return None

        return super().address_record_to_dict(record)
