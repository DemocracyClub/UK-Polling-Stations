from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000220'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Rugby.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Rugby.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '10010523748':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'CV22 7EX'
            return rec

        return super().address_record_to_dict(record)
