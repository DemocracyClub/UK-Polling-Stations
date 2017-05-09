from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'W06000009'
    districts_name = 'PollingDistrictWithStation Pembrokeshire for 2017/PollingDistrictWithStation'
    stations_name = 'PollingDistrictWithStation Pembrokeshire for 2017/PollingDistrictWithStation.shp'
    elections = [
        'local.pembrokeshire.2017-05-04',
        'parl.2017-06-08'
    ]

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': str(record[1]).strip(),
            'name': str(record[2]).strip()
        }

    def station_record_to_dict(self, record):
        station = {
            'internal_council_id': str(record[1]).strip(),
            'postcode': '',
            'address': str(record[4]).strip(),
            'polling_district_id': str(record[1]).strip(),
        }

        """
        This file doesn't actually have points for stations
        and we want to ensure that we don't try to insert
        the polygon data into the location field
        """
        station ['location'] = None

        return station
