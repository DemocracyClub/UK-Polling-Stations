from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000009'
    addresses_name = 'local.2018-05-03/Version 1/Ealing Polling Station Finder Democracy_Club__03May2018.TSV'
    stations_name = 'local.2018-05-03/Version 1/Ealing Polling Station Finder Democracy_Club__03May2018.TSV'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip('0')

        if uprn in ['12160219', '12171951']:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'W3 9QB'
            return rec

        if record.addressline6 == 'UB5 6XJ':
            return None

        if uprn in ['12116009', '12116010', '12116011']:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'W3 8EJ'
            return rec

        return super().address_record_to_dict(record)
