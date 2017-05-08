from data_collection.morph_importer import BaseMorphApiImporter

class Command(BaseMorphApiImporter):

    srid = 4326
    districts_srid  = 4326
    council_id = 'E07000062'
    elections = ['parl.2017-06-08']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Hastings'
    geom_type = 'geojson'

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))
        code = record['elbcode'].strip()
        return {
            'internal_council_id': code,
            'name': record['elbname'].strip() + ' - ' + code,
            'area': poly,
            'polling_station_id': code,
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(record, self.geom_type, self.get_srid('stations'))
        return {
            'internal_council_id': record['district'].strip(),
            'postcode': '',
            'address': record['location'].strip(),
            'location': location,
        }
