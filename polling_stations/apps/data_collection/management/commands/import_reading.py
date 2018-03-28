from data_collection.management.commands import BaseXpressDCCsvInconsistentPostcodesImporter

class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = 'E06000038'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Reading.CSV'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Reading.CSV'
    elections = ['local.2018-05-03']
    csv_delimiter = ','

    def address_record_to_dict(self, record):
        if record.property_urn.strip() in ['310082434', '310082435']:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'RG2 6AB'
            return rec

        if record.property_urn.strip() == '310074687':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'RG1 5NN'
            return rec

        if record.property_urn.strip() == '310080353':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'RG6 1DJ'
            return rec

        return super().address_record_to_dict(record)
