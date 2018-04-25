from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id      = 'E08000004'
    addresses_name  = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Oldham.tsv'
    stations_name   = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Oldham.tsv'
    elections       = ['local.2018-05-03']
    csv_delimiter = '\t'


    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '422000018374':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'OL9 9PW'
            return rec

        if uprn == '422000006570':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'OL9 9BA'
            return rec

        if record.addressline6 == 'OL3 5GL':
            return None

        if uprn == '422000046844':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'OL2 5DR'
            return rec

        if uprn == '422000011979':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'OL9 0EW'
            return rec

        if uprn == '422000076707':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'OL4 5LN'
            return rec

        if uprn == '422000044527':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'OL8 4QG'
            return rec

        if uprn == '422000104304':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'OL9 9DX'
            return rec

        if uprn == '422000086761':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'OL4 1NQ'
            return rec

        return super().address_record_to_dict(record)
