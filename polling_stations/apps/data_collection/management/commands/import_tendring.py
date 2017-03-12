from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'E07000076'
    districts_name = 'PollingDistricts2016'
    stations_name = 'Polling_Stations_Tendring_2017.shp'
    elections = ['local.essex.2017-05-04']

    def district_record_to_dict(self, record):
        name = str(record[4]).strip()
        code = name[:2]
        return {
            'internal_council_id': code,
            'name': name,
            'polling_station_id': code,
        }

    def station_record_to_dict(self, record):
        return {
            'internal_council_id': str(record[2]).strip(),
            'postcode': '',
            'address': str(record[1]).strip(),
        }
