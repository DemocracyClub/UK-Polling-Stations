from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000041'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Exeter.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Exeter.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def station_record_to_dict(self, record):

        if record.polling_place_id == '3400':
            record = record._replace(polling_place_easting = '290734')
            record = record._replace(polling_place_northing = '91778')

        if record.polling_place_id == '3257':
            record = record._replace(polling_place_easting = '')
            record = record._replace(polling_place_northing = '')

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip('0')

        if record.addressline6.strip() == 'EX2 7PU':
            return None

        if uprn == '100041143711':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'EX4 7AY'
            return rec

        if record.addressline6.strip() == 'EX5 4BH':
            return None

        if record.addressline6.strip() == 'EX2 7PU':
            return None

        return super().address_record_to_dict(record)
