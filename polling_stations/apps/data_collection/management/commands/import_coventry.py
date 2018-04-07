from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E08000026'
    addresses_name  = 'local.2018-05-03/Version 1/PropertyPostCodePollingStationWebLookup-2018-03-19.TSV'
    stations_name   = 'local.2018-05-03/Version 1/PropertyPostCodePollingStationWebLookup-2018-03-19.TSV'
    elections       = ['local.2018-05-03']
    csv_delimiter = '\t'

    def station_record_to_dict(self, record):

        if record.pollingplaceid == '8900':
            record = record._replace(pollingplaceaddress7 = 'CV3 2SB')

        if record.pollingplaceid == '8890':
            record = record._replace(pollingplaceaddress7 = 'CV5 7LR')

        if record.pollingplaceid == '8636':
            record = record._replace(pollingplaceaddress7 = 'CV6 4GF')

        if record.pollingplaceid == '8843':
            rec = super().station_record_to_dict(record)
            rec['location'] = Point(-1.5647868, 52.3814416, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        uprn = record.uprn.strip().lstrip('0')
        if uprn == '10024028272':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'CV6 6BL'
            return rec

        return super().address_record_to_dict(record)
