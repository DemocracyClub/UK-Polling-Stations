from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000072'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (1) Epping Forest.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (1) Epping Forest.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip('0')

        if record.addressline6.strip() == 'IG10 2DY':
            return None

        if record.addressline6.strip() == 'CM5 0QG':
            return None

        if uprn == '200001862939':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'CM16 5HF'
            return rec

        return super().address_record_to_dict(record)
