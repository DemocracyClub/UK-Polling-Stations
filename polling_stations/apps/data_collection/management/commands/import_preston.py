from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id      = 'E07000123'
    addresses_name  = 'local.2018-05-03/Version 1/Democracy_Club__03May2018.CSV'
    stations_name   = 'local.2018-05-03/Version 1/Democracy_Club__03May2018.CSV'
    elections       = ['local.2018-05-03']
    csv_delimiter   = ','

    def station_record_to_dict(self, record):

        if record.polling_place_id == '2242':
            record = record._replace(polling_place_postcode='PR3 2BH')
            record = record._replace(polling_place_easting = '0')
            record = record._replace(polling_place_northing = '0')

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '10002223992':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'PR2 6YH'
            return rec

        return super().address_record_to_dict(record)
