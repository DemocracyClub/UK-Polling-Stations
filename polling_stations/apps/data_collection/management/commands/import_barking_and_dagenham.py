from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000002'
    addresses_name = 'local.2018-05-03/Version 3/EC & Democracy Club Polling Place Lookup Barking and Dagenham.csv'
    stations_name = 'local.2018-05-03/Version 3/EC & Democracy Club Polling Place Lookup Barking and Dagenham.csv'
    elections = ['local.2018-05-03']

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip('0')

        if record.addressline6 == 'IG11 8RF':
            return None

        barnmead = [
            '100001639',
            '100001637',
            '100001635',
            '100001633',
            '100001631',
            '100001629',
            '100001627',
            '100001624',
            '100001622',
        ]
        if uprn in barnmead:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'RM9 5DX'
            return rec

        if uprn == '100012133':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'RM8 1DJ'
            return rec

        if uprn == '100033274':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'IG11 9ES'
            return rec

        if uprn == '100041457':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'RM10 9BX'
            return rec

        if uprn == '100033020':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'RM6 6RJ'
            return rec

        if uprn == '10002171985':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'RM10 7XJ'
            return rec

        return super().address_record_to_dict(record)
