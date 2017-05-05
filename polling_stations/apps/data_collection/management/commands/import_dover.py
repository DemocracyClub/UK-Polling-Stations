from django.contrib.gis.geos import Point
from data_collection.morph_importer import BaseMorphApiImporter


class Command(BaseMorphApiImporter):

    srid = 27700
    districts_srid  = 4326
    council_id = 'E07000108'
    elections = ['parl.2017-06-08']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Dover'
    geom_type = 'geojson'

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))
        return {
            'internal_council_id': record['code'],
            'name': record['district'],
            'area': poly,
            'polling_station_id': record['code'],
        }

    def station_record_to_dict(self, record):

        location = Point(
            float(record['EASTING']),
            float(record['NORTHING']),
            srid=self.get_srid('stations')
        )
        address = "\n".join([
            record['NAME_OF_PO'],
            record['LOCATION'],
        ])

        return {
            'internal_council_id': record['POLLING_DI'],
            'postcode': record['POSTCODE'],
            'address': address,
            'location': location,
        }
