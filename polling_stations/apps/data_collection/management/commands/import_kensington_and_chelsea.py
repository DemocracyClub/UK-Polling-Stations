from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id       = 'E09000020'
    addresses_name   = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (1) Kensington and Chelsea.CSV'
    stations_name    = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (1) Kensington and Chelsea.CSV'
    elections        = ['local.2018-05-03']

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '217102607':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'W11 4NH'
            return rec

        if record.addressline6 == 'W11 4LY' and\
                record.addressline1 == '2 (B)' and\
                record.addressline2 == 'Drayson Mews':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'W8 4LY'
            return rec

        if record.addressline6 == 'W11 1PZ' and uprn == '':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'W11 4PZ'
            return rec

        return super().address_record_to_dict(record)
