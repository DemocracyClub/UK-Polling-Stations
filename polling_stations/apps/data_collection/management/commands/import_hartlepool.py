from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E06000001'
    addresses_name  = 'HartlepoolProperty Post Code New.csv'
    stations_name   = 'HartlepoolProperty Post Code New.csv'
    elections       = ['mayor.tees-valley.2017-05-04']

    # Hartlepool use Xpress, but they've provided a slightly trimmed down
    # version of the WebLookup export. We need to customise a bit..

    station_postcode_field = None
    station_address_fields = [
        'pollingplaceaddress1',
        'pollingplaceaddress2',
    ]
    station_id_field = 'pollingplaceid'
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
