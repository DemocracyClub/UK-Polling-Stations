from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000030'
    addresses_name = 'local.2018-05-03/Version 2/Democracy_Club__03May2018.tsv'
    stations_name = 'local.2018-05-03/Version 2/Democracy_Club__03May2018.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'
    csv_encoding = 'windows-1252'

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '6198433':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'E2 9DG'
            return rec

        if record.addressline6 == 'E3 2LB' or record.addressline6 == 'E3 5EG':
            return None

        return super().address_record_to_dict(record)
