from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000025'
    addresses_name = 'local.2018-05-03/Version 2/LBNewham Democracy_Club__03May2018.TSV'
    stations_name = 'local.2018-05-03/Version 2/LBNewham Democracy_Club__03May2018.TSV'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):

        if record.addressline6 == 'E16 1EF':
            return None

        if record.property_urn == '10090852604':
            return None

        if record.property_urn == '10034510101':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'E13 8NA'
            return rec

        if record.addressline6 == 'E16 1XF':
            return None

        if record.property_urn == '10090756946':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'E7 9AW'
            return rec

        if record.property_urn == '10023994990':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'E7 9AW'
            return rec

        return super().address_record_to_dict(record)
