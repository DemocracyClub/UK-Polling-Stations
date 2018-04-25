from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id      = 'E06000001'
    addresses_name  = 'local.2018-05-03/Version 1/Tracy  Test Democracy_Club__03May2018.CSV'
    stations_name   = 'local.2018-05-03/Version 1/Tracy  Test Democracy_Club__03May2018.CSV'
    elections       = ['local.2018-05-03']

    # Hartlepool use Xpress, but they've provided a slightly trimmed down
    # version of the export. We need to customise a bit..

    station_postcode_field = None
    station_address_fields = [
        'polling_place_name',
        'polling_place_address_1',
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

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        if rec:
            rec['uprn'] = ''
        return rec
