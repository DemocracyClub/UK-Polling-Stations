from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E07000145'
    addresses_name  = 'local.2018-05-03/Version 1/polling_station_export-2018-04-20.csv'
    stations_name   = 'local.2018-05-03/Version 1/polling_station_export-2018-04-20.csv'
    elections       = ['local.2018-05-03']
    csv_encoding    = 'windows-1252'

    def station_record_to_dict(self, record):

        if record.pollingstationnumber == '15':
            record = record._replace(pollingstationpostcode='')

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip('0')

        if record.houseid == '48125':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NR31 9EP'
            return rec

        if uprn == '100091559681':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NR29 3PF'
            return rec

        if uprn == '10012182814':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NR31 9FH'
            return rec

        if uprn == '10012179821':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NR30 3LD'
            return rec

        if uprn == '10012182400':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NR31 9EB'
            return rec

        if record.houseid == '46097':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NR31 6LP'
            return rec

        if uprn == '10023460781':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NR29 3DG'
            return rec

        if uprn == '10023466148':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NR30 1EL'
            return rec

        if uprn == '10023466449':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NR30 2GB'
            return rec

        if uprn == '10012180406':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NR29 4JL'
            return rec

        if uprn in ['100091318449', '100091616205']:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NR29 4HZ'
            return rec

        if record.houseid == '48177':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NR31 6SG'
            return rec

        if record.houseid == '48376':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NR31 6QT'
            return rec

        if uprn == '10023460310':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NR31 9FN'
            return rec

        if record.houseid == '48841':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'NR30 3AY'
            return rec

        return super().address_record_to_dict(record)
