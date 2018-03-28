from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E08000030'
    addresses_name  = 'local.2018-05-03/Version 2/polling_station_export-2018-03-12.csv'
    stations_name   = 'local.2018-05-03/Version 2/polling_station_export-2018-03-12.csv'
    elections       = ['local.2018-05-03']
    csv_encoding    = 'windows-1252'

    def address_record_to_dict(self, record):
        if record.houseid in ['123217', '123218', '123219']:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'WS9 0BA'
            return rec

        if record.houseid == '117495':
            rec = super().address_record_to_dict(record)
            rec['polling_station_id'] = ''
            return rec

        if record.housepostcode == 'WS9 9DE':
            return None

        if record.housepostcode == 'WS1 3DS':
            return None

        return super().address_record_to_dict(record)
