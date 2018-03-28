from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000062'
    addresses_name  = 'local.2018-05-03/Version 1/polling_station_export-2018-03-12.csv'
    stations_name   = 'local.2018-05-03/Version 1/polling_station_export-2018-03-12.csv'
    elections       = ['local.2018-05-03']
    csv_encoding    = 'windows-1252'

    def address_record_to_dict(self, record):
        if record.houseid == '3000023':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'TN38 0BN'
            return rec

        if record.houseid == '5000237':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'TN37 6BP'
            return rec

        return super().address_record_to_dict(record)
