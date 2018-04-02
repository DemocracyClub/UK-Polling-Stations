from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000012'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018  South Cambridge.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018  South Cambridge.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '10003189372':
            return None

        if uprn == '100090137727':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'CB24 8QG'
            return rec

        if uprn == '10033034680':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'CB21 5AE'
            return rec

        return super().address_record_to_dict(record)
