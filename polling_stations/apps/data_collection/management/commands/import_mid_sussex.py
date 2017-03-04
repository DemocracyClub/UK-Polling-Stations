from data_collection.morph_importer import BaseMorphApiImporter

class Command(BaseMorphApiImporter):

    srid = 4326
    districts_srid  = 4326
    council_id = 'E07000228'
    elections = ['local.west-sussex.2017-05-04']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Mid-Sussex'
    geom_type = 'geojson'
    split_districts = set()

    def get_station_hash(self, record):
        # handle exact dupes on code/address
        return "-".join([
            record['msercode'],
            record['postcode'],
        ])

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))
        return {
            'internal_council_id': record['msercode'],
            'name'               : record['boundname'],
            'area'               : poly,
            'polling_station_id' : record['msercode'],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(record, self.geom_type, self.get_srid('stations'))

        codes = record['msercode'].split("/")
        stations = []
        for code in codes:
            stations.append({
                'internal_council_id': code.strip(),
                'postcode':            record['postcode'],
                'address':             "\n".join([record['venue'], record['street'], record['town']]),
                'location':            location,
            })

        return stations
