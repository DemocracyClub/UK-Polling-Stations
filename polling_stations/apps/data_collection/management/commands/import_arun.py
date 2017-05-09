from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'E07000224'
    districts_name = 'shp/AR_RE_PollingDistricts2017'
    stations_name = 'shp/AR_RE_PollingStations2017.shp'
    elections = [
        'local.west-sussex.2017-05-04',
        'parl.2017-06-08'
    ]

    def district_record_to_dict(self, record):
        code = str(record[0]).strip()
        return {
            'internal_council_id': code,
            'name': str(record[1]).strip(),
            'polling_station_id': code,
        }

    def station_record_to_dict(self, record):

        return {
            'internal_council_id': str(record[1]).strip(),
            'postcode': '',
            'address': str(record[7]).strip(),
        }
