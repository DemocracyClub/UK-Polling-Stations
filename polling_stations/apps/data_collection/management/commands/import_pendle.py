from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000122'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Pendle.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Pendle.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip('0')

        if record.addressline6 == 'BB9 5LQ' and record.addressline1 == '14 Walton Place':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'BB9 8DQ'
            return rec

        return super().address_record_to_dict(record)
