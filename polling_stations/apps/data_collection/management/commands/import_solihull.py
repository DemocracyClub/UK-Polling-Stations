from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E08000029'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Solihull.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Solihull.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip('0')

        if record.addressline6 == 'CV7 7SQ':
            return None

        if uprn == '10090945566':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'B94 6BD'
            return rec

        if uprn in ['10090946240', '10090946268']:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'B93 8NA'
            return rec

        if uprn in ['10008211727', '10008211728']:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'B91 2JJ'
            return rec

        if record.addressline6 == 'CV7 7HN':
            return None

        if record.addressline6 == 'CV7 7HL':
            return None

        return super().address_record_to_dict(record)
