from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id      = 'E08000002'
    addresses_name  = 'local.2018-05-03/Version 1/Democracy Club PS DETAILS.csv'
    stations_name   = 'local.2018-05-03/Version 1/Democracy Club PS DETAILS.csv'
    elections       = ['local.2018-05-03']

    def station_record_to_dict(self, record):

        if record.polling_place_id == '2574':
            record = record._replace(polling_place_postcode='BL0 0BJ')

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip('0')

        if uprn in ['100010957935', '100010957934']:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'BL9 6JW'
            return rec

        if record.addressline6 == 'BL9 9JN':
            return None

        if record.addressline6 == 'BL8 4LA':
            return None

        if record.addressline6 == 'M26 1FP':
            return None

        if record.addressline6 == 'BL8 2HH':
            return None

        return super().address_record_to_dict(record)
