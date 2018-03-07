from data_collection.github_importer import BaseGitHubImporter

class Command(BaseGitHubImporter):

    srid = 4326
    districts_srid  = 4326
    council_id = 'E08000006'
    elections = ['local.2018-05-03']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Salford'
    geom_type = 'geojson'

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))
        return {
            'internal_council_id': record['code'],
            'name'               : record['code'],
            'area'               : poly
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(record, self.geom_type, self.get_srid('stations'))
        return {
            'internal_council_id': record['polling_district'],
            'postcode':            '',
            'address':             record['station_location'],
            'location':            location,
            'polling_district_id': record['polling_district']
        }
