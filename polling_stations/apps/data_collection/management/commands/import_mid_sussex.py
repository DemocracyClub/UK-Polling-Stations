from data_collection.morph_importer import BaseMorphApiImporter

class Command(BaseMorphApiImporter):

    srid = 4326
    districts_srid  = 4326
    council_id = 'E07000228'
    elections = ['local.west-sussex.2017-05-04']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Mid-Sussex'
    geom_type = 'geojson'
    split_districts = set()

    def pre_import(self):
        self.find_split_districts()

    def get_station_hash(self, record):
        # handle exact dupes on code/address
        return "-".join([
            record['msercode'],
            record['uprn']
        ])

    def find_split_districts(self):
        # identify any district codes which appear more than once
        # with 2 different polling station addresses.
        # We do not want to import these.
        stations = self.get_stations()
        for station1 in stations:
            for station2 in stations:
                if (station2['msercode'] == station1['msercode'] and\
                    station2['uprn'] != station1['uprn']):
                    self.split_districts.add(station1['msercode'])

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))
        return {
            'internal_council_id': record['msercode'],
            'name'               : record['boundname'],
            'area'               : poly,
            'polling_station_id' : record['msercode'],
        }

    def station_record_to_dict(self, record):

        # handle split districts
        if record['msercode'] in self.split_districts:
            return None

        location = self.extract_geometry(record, self.geom_type, self.get_srid('stations'))
        return {
            'internal_council_id': record['msercode'],
            'postcode':            '',
            'address':             record['address'],
            'location':            location,
        }
