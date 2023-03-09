from data_importers.base_importers import BaseShpStationsShpDistrictsImporter


class Command(BaseShpStationsShpDistrictsImporter):
    council_id = "LAC"
    elections = ["2023-05-04"]
    srid = 27700
    districts_name = "2023-05-04/2023-03-29T14:36:00/PollingDistandStat.shp"
    stations_name = "2023-05-04/2023-03-29T14:36:00/LancasterPollingStations2023.shp"

    def district_record_to_dict(self, record):
        return {"internal_council_id": record[0], "name": f"{record[2]} - {record[0]}"}

    def station_record_to_dict(self, record):
        return {
            "internal_council_id": record[0],
            "address": record[1],
            "postcode": "",
            "polling_district_id": record[0],
        }
