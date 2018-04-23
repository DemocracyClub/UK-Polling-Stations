from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000010'
    addresses_name = 'local.2018-05-03/Version 1/Democracy Counts Polling Place Lookup Enfield.csv'
    stations_name = 'local.2018-05-03/Version 1/Democracy Counts Polling Place Lookup Enfield.csv'
    elections = ['local.2018-05-03']
    csv_delimiter = ','

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '207086112':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'N13 4AP'
            return rec

        if uprn == '207017348':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'N21 2AU'
            return rec

        if uprn == '207083595':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'N21 2SD'
            return rec

        return super().address_record_to_dict(record)
