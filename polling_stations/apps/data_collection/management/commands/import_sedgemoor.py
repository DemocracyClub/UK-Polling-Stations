from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000188'
    addresses_name  = 'Sedgemoor_polling_station_export-2017-02-24.csv'
    stations_name   = 'Sedgemoor_polling_station_export-2017-02-24.csv'
    elections       = ['local.somerset.2017-05-04']

    def station_record_to_dict(self, record):
        if getattr(record, self.station_id_field).strip() == 'n/a':
            return None
        return super().station_record_to_dict(record)
