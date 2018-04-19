from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id      = 'E07000127'
    addresses_name  = 'local.2018-05-03/Version 1/WLBC-Democracy_Club__03May2018 West Lancashire.TSV'
    stations_name   = 'local.2018-05-03/Version 1/WLBC-Democracy_Club__03May2018 West Lancashire.TSV'
    elections       = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '10012344883':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'L40 9RL'
            return rec

        return super().address_record_to_dict(record)
