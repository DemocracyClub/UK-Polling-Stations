from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id = 'E07000031'
    addresses_name = 'local.2018-05-03/Version 1/polling_station_export-2018-04-03 South Lakeland.csv'
    stations_name = 'local.2018-05-03/Version 1/polling_station_export-2018-04-03 South Lakeland.csv'
    elections = ['local.2018-05-03']

    def address_record_to_dict(self, record):

        # All of the UPRN data from South Lakeland is a bit dubious.
        # For safety I'm just going to ignore them all
        record = record._replace(uprn='')

        return super().address_record_to_dict(record)
