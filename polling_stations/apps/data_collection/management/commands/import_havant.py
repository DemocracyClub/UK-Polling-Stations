from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000090'
    addresses_name = 'local.2018-05-03/Version 2/Democracy_Club__03May2018.tsv'
    stations_name = 'local.2018-05-03/Version 2/Democracy_Club__03May2018.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'
    csv_encoding = 'windows-1252'

    def address_record_to_dict(self, record):
        if record.addressline6 == 'PO11 0PJ':
            return None
        return super().address_record_to_dict(record)
