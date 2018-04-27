from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000028'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '10013527769':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SE15 2DL'
            return rec

        if uprn in  ['200003487670', '200003487907']:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SE1 2BB'
            return rec

        if uprn == '200003462475':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SE5 8PE'
            return rec

        if uprn == '10090283768':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SE1 3UN'
            return rec

        if uprn == '10093341734':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SE1 6PS'
            return rec

        if uprn == '10091665680':
            rec = super().address_record_to_dict(record)
            rec['uprn'] = ''
            rec['postcode'] = 'SE5 0EZ'
            return rec

        if uprn in ['10093341594', '10093341595']:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SE1 2BX'
            return rec

        if uprn == '10093341408':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SE15 4LB'
            return rec

        if uprn == '10093340235':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SE22 9EE'
            return rec

        if record.addressline6 == 'SE5 8FF':
            return None

        if uprn == '10091664197':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SE22 9PP'
            return rec

        if uprn == '10090750130':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SE1 5AD'
            return rec

        return super().address_record_to_dict(record)
