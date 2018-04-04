from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id      = 'E08000007'
    addresses_name  = 'local.2018-05-03/Version 2/Democracy_Club__03May2018.tsv'
    stations_name   = 'local.2018-05-03/Version 2/Democracy_Club__03May2018.tsv'
    elections       = ['local.2018-05-03']
    csv_delimiter   = '\t'

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip('0')

        if record.addressline6 == 'SK7 5AJ':
            return None

        if uprn in ['100011528043', '100011528044', '100011528045']:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SK6 5BT'
            return rec

        if record.addressline6 == 'SK4 4NZ':
            return None

        if uprn == '100011510461':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SK6 3EN'
            return rec

        return super().address_record_to_dict(record)
