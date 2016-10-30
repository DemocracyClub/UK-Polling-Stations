from data_collection.management.commands import BaseMorphApiImporter

class Command(BaseMorphApiImporter):

    srid = 27700
    districts_srid  = 27700
    council_id = 'E07000208'
    elections = ['local.surrey.2017-05-04']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-EpsomAndEwell'
    geom_type = 'gml'

    def get_station_hash(self, record):
        # handle exact dupes on code/address
        return "-".join([
            record['wardname'],
            record['uprn']
        ])

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))
        return {
            'internal_council_id': record['wardcode'],
            'name'               : record['wardcode'],
            'area'               : poly,
            'polling_station_id' : record['wardcode'],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(record, self.geom_type, self.get_srid('stations'))
        return {
            'internal_council_id': record['wardname'],
            'postcode':            '',
            'address':             record['address'],
            'location':            location,
        }
