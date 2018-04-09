from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000084'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Basingstoke.CSV'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Basingstoke.CSV'
    elections = ['local.2018-05-03']
    csv_delimiter = ','

    def address_record_to_dict(self, record):

        if record.addressline6.strip() == 'RG24 7AY':
            return None

        return super().address_record_to_dict(record)
