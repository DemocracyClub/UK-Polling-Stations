from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseCsvStationsJsonDistrictsImporter

class Command(BaseCsvStationsJsonDistrictsImporter):
    srid = 27700
    districts_srid = 27700
    council_id = 'E07000089'
    districts_name = 'Hart Polling Districts-fixed.geojson'
    stations_name = 'Hart Polling Stations 2017 v2 070417-fixed.csv'
    elections = [
        'local.hampshire.2017-05-04',
        'parl.2017-06-08'
    ]

    def district_record_to_dict(self, record):
        name = str(record['properties']['Name']).strip()
        code = name.split(' ')[1]
        return {
            'internal_council_id': code,
            'name': name,
        }

    def station_record_to_dict(self, record):
        location = Point(float(record.easting), float(record.northing), srid=self.srid)
        stations = []
        district_ids = record.districts.split(',')
        district_ids = [d.strip() for d in district_ids]
        for district_id in district_ids:
            stations.append({
                'internal_council_id': district_id,
                'address' : record.polling_place,
                'postcode': record.postcode,
                'polling_district_id': district_id,
                'location': location,
            })
        return stations
