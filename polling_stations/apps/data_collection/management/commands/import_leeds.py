from data_collection.morph_importer import BaseMorphApiImporter

class Command(BaseMorphApiImporter):

    srid = 4326
    districts_srid  = 4326
    council_id = 'E08000035'
    elections = []
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Leeds'
    geom_type = 'geojson'
    split_districts = set()

    def pre_import(self):
        self.find_split_districts()

    def find_split_districts(self):
        'Identify districts mapped to more than one polling station.'
        stations = self.get_stations()
        for station1 in stations:
            for station2 in stations:
                if station1['POLLING_DI'] == station2['POLLING_DI'] and\
                    station1['OBJECTID'] != station2['OBJECTID']:
                    self.split_districts.add(station1['POLLING_DI'])

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))
        return {
            'internal_council_id': record['POLLING_DI'],
            'name': '%s - %s' % (record['WARD'], record['POLLING_DI']),
            'area': poly
        }

    def station_record_to_dict(self, record):

        # Handle split districts
        if record['POLLING_DI'] in self.split_districts:
            return None

        location = self.extract_geometry(record, self.geom_type, self.get_srid('stations'))
        internal_ids = record['POLLING_DI'].split("-")

        if len(internal_ids) == 1:
            return {
                'internal_council_id': record['POLLING_DI'],
                'postcode': '',
                'address': record['POLLING_ST'],
                'location': location,
                'polling_district_id': record['POLLING_DI']
            }
        else:
            stations = []
            for id in internal_ids:
                stations.append({
                    'internal_council_id': id,
                    'postcode': '',
                    'address': record['POLLING_ST'],
                    'location': location,
                    'polling_district_id': id
                })
            return stations
