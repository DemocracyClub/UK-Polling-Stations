from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000103'
    addresses_name  = 'local.2018-05-03/Version 1/polling_station_export-2018-04-06.csv'
    stations_name   = 'local.2018-05-03/Version 1/polling_station_export-2018-04-06.csv'
    elections       = ['local.2018-05-03']
    csv_encoding    = 'windows-1252'

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip('0')

        if uprn in ['100080947255', '100080947259']:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'WD18 7JT'
            return rec

        return super().address_record_to_dict(record)
