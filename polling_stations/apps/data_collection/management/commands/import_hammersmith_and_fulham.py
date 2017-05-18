from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'E09000013'
    districts_name = 'parl.2017-06-08/Version 1/POLLING_HF/POLLING_DISTRICTS'
    stations_name = 'parl.2017-06-08/Version 1/POLLING_HF/POLLING_STATIONS.shp'
    elections = ['parl.2017-06-08']

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[1].strip(),
            'name': record[1].strip(),
            'polling_station_id': record[1].strip(),
        }

    def station_record_to_dict(self, record):
        return {
            'internal_council_id': record[1].strip(),
            'postcode': record[3].strip(),
            'address': record[2].strip(),
        }
