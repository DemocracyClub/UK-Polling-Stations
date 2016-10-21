from data_collection.management.commands import BaseMorphApiImporter

class Command(BaseMorphApiImporter):

    srid = 4326
    districts_srid  = 4326
    council_id = 'E09000009'
    elections = [
        'gla.c.2016-05-05',
        'gla.a.2016-05-05',
        'mayor.london.2016-05-05',
        'ref.2016-06-23',
    ]
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Ealing'
    geom_type = 'geojson'

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))
        return {
            'internal_council_id': record['distcode'],
            'name'               : "%s - %s" % (record['wardname'], record['distcode']),
            'area'               : poly
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(record, self.geom_type, self.get_srid('stations'))
        return {
            'internal_council_id': record['pollingdistrict'],
            'postcode':            '',
            'address':             record['polling_station'],
            'location':            location,
            'polling_district_id': record['pollingdistrict']
        }
