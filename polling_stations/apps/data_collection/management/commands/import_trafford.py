from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id      = 'E08000009'
    addresses_name  = 'local.2018-05-03/Version 2/Democracy_Club__03May2018.tsv'
    stations_name   = 'local.2018-05-03/Version 2/Democracy_Club__03May2018.tsv'
    elections       = ['local.2018-05-03']
    csv_delimiter   = '\t'

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip('0')

        if record.addressline6 == 'M33 5RJ':
            return None

        if uprn == '100012491068':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'WA14 5RJ'
            return rec

        if record.addressline6 == 'WA13 9TY':
            return None

        return super().address_record_to_dict(record)
