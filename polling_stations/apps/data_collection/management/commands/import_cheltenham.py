from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000078'
    addresses_name  = 'local.2018-05-03/Version 1/polling_station_export-2018-04-20 Cheltenham.csv'
    stations_name   = 'local.2018-05-03/Version 1/polling_station_export-2018-04-20 Cheltenham.csv'
    elections       = ['local.2018-05-03']
    csv_encoding    = 'windows-1252'

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip('0')

        if uprn in ['100121231365', '100121231366']:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'GL51 6QL'
            return rec

        if uprn == '100120389274':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'GL52 2BT'
            return rec

        if record.houseid == '63059':
            return None

        return super().address_record_to_dict(record)
