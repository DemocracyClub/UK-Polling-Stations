from data_collection.github_importer import BaseGitHubImporter

class Command(BaseGitHubImporter):

    srid = 4326
    districts_srid  = 4326
    council_id = 'E09000022'
    elections = ['parl.2017-06-08']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Lambeth'
    geom_type = 'geojson'

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))
        return {
            'internal_council_id': record['DISTRICT_CODE'],
            'name': "%s - %s" % (record['WARD'], record['DISTRICT_CODE']),
            'area': poly,
            'polling_station_id': record['DISTRICT_CODE'],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(record, self.geom_type, self.get_srid('stations'))
        return {
            'internal_council_id': record['DISTRICT_C'],
            'postcode': record['POSTCODE'],
            'address': "%s\n%s" % (record['VENUE'], record['ADDRESS']),
            'location': location,
        }
