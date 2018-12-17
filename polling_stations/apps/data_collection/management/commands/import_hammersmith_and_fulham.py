from data_collection.management.commands import BaseShpStationsShpDistrictsImporter


class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = "E09000013"
    districts_name = "parl.2017-06-08/Version 1/POLLING_HF/POLLING_DISTRICTS"
    stations_name = "local.2018-05-03/Version 1/PollingStations.shp"
    elections = ["local.2018-05-03"]

    def district_record_to_dict(self, record):
        return {
            "internal_council_id": record[1].strip(),
            "name": record[1].strip(),
            "polling_station_id": record[1].strip(),
        }

    def station_record_to_dict(self, record):
        return {
            "internal_council_id": record[2].strip(),
            "postcode": record[4].strip(),
            "address": record[3].strip(),
        }
