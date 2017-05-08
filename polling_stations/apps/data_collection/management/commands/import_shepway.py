from data_collection.morph_importer import BaseMorphApiImporter

class Command(BaseMorphApiImporter):

    srid = 4326
    districts_srid  = 4326
    council_id = 'E07000112'
    elections = ['parl.2017-06-08']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Shepway'
    geom_type = 'geojson'

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))
        code = record['dist_code'].strip()
        return {
            'internal_council_id': code,
            'name': record['district_n'].strip() + ' - ' + code,
            'area': poly,
            'polling_station_id': code,
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(record, self.geom_type, self.get_srid('stations'))
        codes = record['polling_di'].split('\\')
        codes = [code.strip() for code in codes]
        stations = []
        for code in codes:
            stations.append({
                'internal_council_id': code,
                'postcode': '',
                'address': record['address'].strip(),
                'location': location,
            })
        return stations
