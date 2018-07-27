from django.contrib.gis.geos.collections import LineString, Point
from data_collection.geo_utils import fix_bad_polygons
from data_collection.github_importer import BaseGitHubImporter


class Command(BaseGitHubImporter):
    srid = 27700
    districts_srid = 27700
    council_id = 'E07000123'
    elections = []
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Preston'
    geom_type = 'geojson'

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(
            record,
            self.geom_type,
            self.get_srid('districts')
        )

        # strip out messy stuff from this layer
        if isinstance(poly, LineString):
            return None
        if isinstance(poly, Point):
            return None

        return {
            'internal_council_id': record['name_5'],
            'name': "%s - %s" % (record['ward'], record['name_5']),
            'area': poly,
            'polling_station_id': record['name_5'],
        }

    def format_address(self, record):
        return "\n".join([
            record['postaladdressline1'] if record['postaladdressline1'] else '',
            record['postaladdressline2'] if record['postaladdressline2'] else '',
            record['postaladdressline3'] if record['postaladdressline3'] else '',
            record['postaladdressline4'] if record['postaladdressline4'] else '',
            record['postaladdressline5'] if record['postaladdressline5'] else '',
        ]).strip()

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record,
            self.geom_type,
            self.get_srid('stations')
        )

        if not isinstance(location, Point):
            return None

        return {
            'internal_council_id': record['ps_polling_area'],
            'address': self.format_address(record),
            'postcode': record['postcode'],
            'location': location,
        }

    def post_import(self):
        fix_bad_polygons()
