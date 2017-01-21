from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'E07000113'
    districts_name = 'shp/Swale Polling Districts'
    stations_name = 'shp/Swale Polling Stations.shp'
    elections = ['local.kent.2017-05-04']

    def district_record_to_dict(self, record):
        code = str(record[0]).strip()
        return {
            'internal_council_id': code,
            'name': str(record[1]).strip(),
            'polling_station_id': code,
        }

    def station_record_to_dict(self, record):

        return {
            'internal_council_id': str(record[0]).strip(),
            'postcode': '',
            'address': str(record[4]).strip(),
        }
