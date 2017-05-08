from data_collection.morph_importer import BaseMorphApiImporter


"""
Note:
This importer provides coverage for 190/193 districts
due to incomplete/poor quality data
"""
class Command(BaseMorphApiImporter):

    srid = 4326
    districts_srid = 4326
    council_id = 'S12000015'
    elections = ['parl.2017-06-08']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Fife'
    geom_type = 'geojson'

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(
            record,
            self.geom_type,
            self.get_srid('districts')
        )

        return {
            'internal_council_id': record['CODE'],
            'name': record['NAME'],
            'area': poly,
            'polling_station_id': record['CODE'],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record,
            self.geom_type,
            self.get_srid('stations')
        )

        return {
            'internal_council_id': record['CODE'],
            'address': record['POLLING_PLACE'],
            'postcode': '',
            'location': location,
        }
