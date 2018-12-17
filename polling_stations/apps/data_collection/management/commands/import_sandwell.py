from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E08000028'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (2) Sandwell.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (2) Sandwell.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):

        if record.addressline6 == 'B70 9QP':
            return None

        return super().address_record_to_dict(record)
