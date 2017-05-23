from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E09000001'
    addresses_name  = 'parl.2017-06-08/Version 1/polling_station_export-2017-05-18.csv'
    stations_name   = 'parl.2017-06-08/Version 1/polling_station_export-2017-05-18.csv'
    elections       = ['parl.2017-06-08']
    csv_encoding    = 'windows-1252'

    def station_record_to_dict(self, record):
        if getattr(record, self.station_id_field).strip() == 'n/a':
            return None
        return super().station_record_to_dict(record)
