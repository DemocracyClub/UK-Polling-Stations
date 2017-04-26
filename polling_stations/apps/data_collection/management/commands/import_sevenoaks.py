from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'E07000111'
    districts_name = 'May 2017/SDC_PollingDistricts_2017'
    stations_name = 'May 2017/SDC_CouncilElecPollingStn2017.shp'
    elections = ['local.kent.2017-05-04']

    def district_record_to_dict(self, record):
        code = str(record[3]).strip()
        return {
            'internal_council_id': code,
            'name': str(record[0]).strip(),
            'polling_station_id': code,
        }

    def station_record_to_dict(self, record):
        return {
            'internal_council_id': str(record[1]).strip(),
            'postcode': '',
            'address': str(record[9]).strip(),
        }
