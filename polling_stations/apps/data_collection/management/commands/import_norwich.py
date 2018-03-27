from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000148'
    addresses_name  = 'local.2018-05-03/Version 1/polling_station_export-2018-03-06.csv'
    stations_name   = 'local.2018-05-03/Version 1/polling_station_export-2018-03-06.csv'
    elections       = ['local.2018-05-03']

    def address_record_to_dict(self, record):

        if record.housepostcode == 'NR1 2EE':
            return None

        if record.houseid == '71720':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NR1 4AB'
            return rec

        return super().address_record_to_dict(record)
