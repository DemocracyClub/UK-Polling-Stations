from django.conf import settings
from data_collection.morph_importer import BaseMorphApiImporter

class Command(BaseMorphApiImporter):

    srid = 27700
    districts_srid  = 27700
    council_id = 'E07000212'
    elections = ['local.surrey.2017-05-04']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Runnymede'
    geom_type = 'gml'

    # stations data has duplicate ids and codes that don't match,
    # but we can grab a valid addresses for each district
    # from the districts file
    @property
    def stations_url(self):
        return "%s%s%s&key=%s" % (
            self.base_url,
            self.scraper_name,
            self.districts_query,
            settings.MORPH_API_KEY,
        )

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))
        return {
            'internal_council_id': record['Poling_Districts'],
            'name'               : record['Poling_Districts'],
            'area'               : poly,
        }

    def station_record_to_dict(self, record):
        location = None
        return {
            'internal_council_id': record['Poling_Districts'],
            'postcode':            '',
            'address':             record['Premises'],
            'location':            location,
            'polling_district_id': record['Poling_Districts']
        }
