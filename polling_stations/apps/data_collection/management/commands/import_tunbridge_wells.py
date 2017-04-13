from data_collection.morph_importer import BaseMorphApiImporter


class Command(BaseMorphApiImporter):

    srid = 4326
    districts_srid = 4326
    council_id = 'E07000116'
    elections = ['local.kent.2017-05-04']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-TunbridgeWells'
    geom_type = 'geojson'

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(
            record,
            self.geom_type,
            self.get_srid('districts')
        )

        return {
            'internal_council_id': record['Letter'],
            'name': record['Polling_Di'],
            'area': poly,
            'polling_station_id': record['Letter'],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record,
            self.geom_type,
            self.get_srid('stations')
        )

        return {
            'internal_council_id': record['Polling_le'],
            'address': record['ADDRESS'],
            'postcode': '',
            'location': location,
        }
