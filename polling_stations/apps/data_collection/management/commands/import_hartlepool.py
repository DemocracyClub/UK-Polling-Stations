from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E06000001'
    addresses_name  = 'parl.2017-06-08/Version 1/Hartlepool Polling Station Addresses for Democracy Club.csv'
    stations_name   = 'parl.2017-06-08/Version 1/Hartlepool Polling Station Addresses for Democracy Club.csv'
    elections       = ['parl.2017-06-08']

    # Hartlepool use Xpress, but they've provided a slightly trimmed down
    # version of the WebLookup export. We need to customise a bit..

    station_postcode_field = None
    station_address_fields = [
        'pollingplaceaddress1',
        'pollingplaceaddress2',
    ]
    station_id_field = 'polling_place_id'
    easting_field = 'pollingplaceeasting'
    northing_field = 'pollingplacenorthing'

    def station_record_to_dict(self, record):
        address = self.get_station_address(record)
        location = None
        return {
            'internal_council_id': getattr(record, self.station_id_field).strip(),
            'postcode'           : '',
            'address'            : address.strip(),
            'location'           : location
        }
