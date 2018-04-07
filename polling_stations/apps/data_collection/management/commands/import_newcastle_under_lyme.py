from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000195'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def station_record_to_dict(self, record):

        # Postcode supplied for Higherland Methodist Church is incorrect
        # remove the grid ref and we'll fall back to UPRN
        if record.polling_place_id == '488':
            record = record._replace(polling_place_easting = '0')
            record = record._replace(polling_place_northing = '0')

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip('0')

        if record.addressline6 == 'CW9 9PW':
            return None

        if uprn == '200004611540':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'TF9 4JG'
            return rec

        if uprn == '200004601964':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'CW3 9LE'
            return rec

        return super().address_record_to_dict(record)
