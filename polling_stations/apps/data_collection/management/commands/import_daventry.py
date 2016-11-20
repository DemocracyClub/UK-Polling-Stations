from django.contrib.gis.geos import GEOSGeometry, Point
from data_collection.geo_utils import convert_linestring_to_multiploygon
from data_collection.management.commands import BaseApiKmlStationsKmlDistrictsImporter

class Command(BaseApiKmlStationsKmlDistrictsImporter):
    srid             = 4326
    districts_srid   = 4326
    council_id       = 'E07000151'
    districts_url    = 'http://feeds.getmapping.com/47732.wmsx?login=61dfb362-893b-464d-8a96-fb3edb7565f8&password=yd5v5y03&LAYERS=daventry_parliamentary_polling_districts_region&TRANSPARENT=TRUE&HOVER=false&FORMAT=kml&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&CRS=EPSG%3A27700&BBOX=447025,247876,489247,288998&WIDTH=867&HEIGHT=426'
    stations_url     = 'http://feeds.getmapping.com/47733.wmsx?login=70a1b086-b9cc-4b22-9b90-7d88bd589d4b&password=sjy2869b&LAYERS=daventry_parliamentary_polling_stations&TRANSPARENT=TRUE&HOVER=false&FORMAT=kml&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&CRS=EPSG%3A27700&BBOX=449708,250805,486927,287603&WIDTH=867&HEIGHT=426'
    elections        = [
        'local.northamptonshire.2017-05-04'
    ]
    duplicate_districts = set()

    def pre_import(self):
        self.find_duplicate_districts()

    def find_duplicate_districts(self):
        # identify any district codes which appear
        # more than once (with 2 different polygons)
        # We do not want to import these.
        seen = set()
        districts = self.get_districts()
        for district in districts:
            if str(district['pollingdis']) in seen:
                self.duplicate_districts.add(str(district['pollingdis']))
            seen.add(str(district['pollingdis']))

    def district_record_to_dict(self, record):
        # polygon
        geojson = record.geom.geojson
        geometry_collection = self.clean_poly(GEOSGeometry(geojson, srid=self.get_srid('districts')))
        poly = convert_linestring_to_multiploygon(geometry_collection)

        district_id = str(record['pollingdis']).strip()
        if district_id in self.duplicate_districts:
            return None
        else :
            return {
                'internal_council_id': district_id,
                'name'               : "%s - %s" % (record['pollingdis'], record['name']),
                'area'               : poly
            }

    def format_address(self, address_parts):
        address = "\n".join(address_parts)
        while "\n\n" in address:
            address = address.replace("\n\n", "\n")
        return address

    def station_record_to_dict(self, record):
        # point
        geojson = record.geom.geojson
        location = GEOSGeometry(geojson, srid=self.get_srid())

        # address
        address = self.format_address([
            str(record['polling_st']),
            ("%s %s" % (str(record['address1']), str(record['address2']))).strip(),
            str(record['locality']),
            str(record['town_villa']),
        ])

        district_ids = str(record['pollingdis']).strip().split(', ')
        stations = []
        for district_id in district_ids:
            stations.append({
                'internal_council_id': district_id,
                'postcode':            record['postcode'],
                'address':             address,
                'location':            location,
                'polling_district_id': district_id
            })
        return stations
