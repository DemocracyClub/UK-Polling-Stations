from data_collection.morph_importer import BaseMorphApiImporter

class Command(BaseMorphApiImporter):

    srid = 4326
    districts_srid  = 4326
    council_id = 'E07000121'
    elections = ['local.lancashire.2017-05-04']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Lancaster'
    geom_type = 'geojson'
    seen_stations = set()

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))
        return {
            'internal_council_id': record['PD_REF'],
            'name'               : record['PD_NAME'],
            'area'               : poly,
            'polling_station_id' : record['PD_REF'],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(record, self.geom_type, self.get_srid('stations'))
        stations = []
        codes = record['DISTRICT'].split(' ')

        for code in codes:
            if (code, record['POLLING_PL']) in self.seen_stations:
                stations.append(None)
            else:
                self.seen_stations.add((code, record['POLLING_PL']))
                stations.append({
                    'internal_council_id': code,
                    'postcode':            '',
                    'address':             record['POLLING_PL'],
                    'location':            location,
                })

        return stations
