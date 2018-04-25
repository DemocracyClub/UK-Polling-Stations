from data_collection.management.commands import BaseXpressDCCsvInconsistentPostcodesImporter

class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = 'E06000033'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 130418.TSV'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 130418.TSV'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '10090460019':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SS1 2HQ'
            return rec

        if uprn == '10024285786':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SS1 2PH'
            return rec

        if uprn == '100090684611':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SS2 6UH'
            return rec

        if uprn == '100090684426':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SS1 3AA'
            return rec

        return super().address_record_to_dict(record)
