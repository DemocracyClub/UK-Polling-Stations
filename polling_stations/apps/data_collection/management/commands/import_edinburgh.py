from data_collection.github_importer import BaseGitHubImporter

class Command(BaseGitHubImporter):

    srid = 4326
    districts_srid = 4326
    council_id = 'S12000036'
    elections = ['parl.2017-06-08']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Edinburgh'
    geom_type = 'geojson'

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(
            record,
            self.geom_type,
            self.get_srid('districts')
        )

        return {
            'internal_council_id': record['Code2016'],
            'name': record['NEWWARD'] + ' - ' + record['Code2016'],
            'area': poly,
            'polling_station_id': record['Code2016'],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record,
            self.geom_type,
            self.get_srid('stations')
        )
        codes = record['LG_PP'].split('/')
        codes = [code.strip() for code in codes]

        stations = []
        for code in codes:
            stations.append({
                'internal_council_id': code,
                'address': "\n".join([record['Polling__1'], record['Address_1']]),
                'postcode': '',
                'location': location,
            })
        return stations
