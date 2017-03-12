from django.contrib.gis.geos import Point
from data_collection.base_importers import BaseStationsDistrictsImporter

class Command(BaseStationsDistrictsImporter):
    stations_filetype = 'geojson'
    districts_filetype = 'shp'
    srid = 27700
    council_id = 'E07000124'
    elections = ['local.lancashire.2017-05-04']
    districts_name = 'Ribble Valley 2017 Polling Disricts/Polling Districts'
    stations_name  = 'Ribble Valley 2017 Polling Stations/Polling Stations-fixed.geojson'

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[0],
            'name': record[1],
        }

    def station_record_to_dict(self, record):
        stations = []

        location = Point(
            record['geometry']['coordinates'][0],
            record['geometry']['coordinates'][1],
            srid=self.srid
        )

        district_codes = []
        if record['properties']['CODE']:
            district_codes.append(record['properties']['CODE'].strip())
        if record['properties']['CODE 2']:
            district_codes.append(record['properties']['CODE 2'].strip())
        if record['properties']['CODE 3']:
            district_codes.append(record['properties']['CODE 3'].strip())

        for code in district_codes:
            stations.append({
                'internal_council_id': code,
                'address': "%s\n%s" % (record['properties']['Name'].strip(), record['properties']['Address'].strip()),
                'postcode': record['properties']['Postcode'].strip(),
                'polling_district_id': code,
                'location': location,
            })

        return stations
