from data_collection.github_importer import BaseGitHubImporter

class Command(BaseGitHubImporter):
    srid = 4326
    council_id = 'E07000172'
    elections = []
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Broxtowe'
    geom_type = 'geojson'

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(
            record,
            self.geom_type,
            self.get_srid('districts')
        )

        return {
            'internal_council_id': record['NAME'],
            'name': ' - '.join([record['WARD_NAME'], record['NAME']]),
            'area': poly,
            'polling_station_id': record['NAME'],
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(
            record,
            self.geom_type,
            self.get_srid('stations')
        )

        id_ = record['POLL_DIST']
        if len(id_.split(' ')) > 1:
            id_ = id_.split(' ')[0]

        if record['ADDRESS'].lower().startswith(record['LABEL'].lower()):
            address = record['ADDRESS']
        else:
            address = "\n".join([record['LABEL'], record['ADDRESS']])

        return {
            'internal_council_id': id_,
            'address': address,
            'postcode': '',
            'location': location,
        }
