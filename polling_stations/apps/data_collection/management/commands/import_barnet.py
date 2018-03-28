from data_collection.management.commands import BaseDemocracyCountsCsvImporter

class Command(BaseDemocracyCountsCsvImporter):
    council_id = 'E09000003'
    addresses_name = 'local.2018-05-03/Version 1/Democracy Club - Polling Districts (1) Barnet.csv'
    stations_name = 'local.2018-05-03/Version 1/Democracy Club - Polling Stations Barnet.csv'
    elections = ['local.2018-05-03']

    def address_record_to_dict(self, record):

        if record.postcode == 'A1 1AA':
            # this is a dummy record
            return None

        if record.uprn == '-2709':
            rec = super().address_record_to_dict(record)
            rec['polling_station_id'] = ''
            return rec

        if record.postcode == 'N20 0RB':
            return None

        return super().address_record_to_dict(record)
