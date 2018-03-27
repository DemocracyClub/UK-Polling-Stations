from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000118'
    addresses_name  = 'local.2018-05-03/Version 1/Eros_SQL_Output001 Chorley.csv'
    stations_name   = 'local.2018-05-03/Version 1/Eros_SQL_Output001 Chorley.csv'
    elections       = ['local.2018-05-03']

    def address_record_to_dict(self, record):

        if record.housepostcode == 'PR6 7ED':
            return None

        if record.houseid == '54062':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'PR7 7FP'
            return rec

        return super().address_record_to_dict(record)
