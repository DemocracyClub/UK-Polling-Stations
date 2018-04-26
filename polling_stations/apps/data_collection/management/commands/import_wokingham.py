from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E06000041'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (1) Wokingham.csv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (1) Wokingham.csv'
    elections = ['local.2018-05-03']
    csv_delimiter = ','

    def station_record_to_dict(self, record):

        if record.polling_place_id == '1347':
            record = record._replace(polling_place_postcode = 'RG6 3HE')

        if record.polling_place_id == '1371':
            record = record._replace(polling_place_postcode = 'RG40 1XS')

        return super().station_record_to_dict(record)
