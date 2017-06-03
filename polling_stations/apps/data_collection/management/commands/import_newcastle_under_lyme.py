from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'E07000195'
    districts_name = 'New data for 4 May/nulbcPollingDistricts'
    stations_name = 'New data for 4 May/nulbcPollingStations.shp'
    elections = [
        'local.staffordshire.2017-05-04',
        #'parl.2017-06-08'
    ]

    def parse_string(self, text):
        try:
            return text.strip().decode('utf-8')
        except AttributeError:
            return text.strip()

    def district_record_to_dict(self, record):
        code = self.parse_string(record[2])
        return {
            'internal_council_id': code,
            'name': "%s - %s" % (self.parse_string(record[1]), code),
            'polling_station_id': code,
        }

    def get_address(self, record):
        if self.parse_string(record[6]):
            return self.parse_string(record[6])
        else:
            return self.parse_string(record[2])

    def station_record_to_dict(self, record):
        code = self.parse_string(record[4])
        if not code:
            return None
        return {
            'internal_council_id': code,
            'postcode': self.parse_string(record[7]),
            'address': self.get_address(record),
        }
