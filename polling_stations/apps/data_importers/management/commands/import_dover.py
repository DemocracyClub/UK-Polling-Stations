from data_importers.base_importers import BaseShpStationsShpDistrictsImporter


class Command(BaseShpStationsShpDistrictsImporter):
    council_id = "DOV"
    stations_name = "2023-05-04/2023-04-27T06:17:27/Polling_Stations.shp"
    stations_filetype = "shp"
    districts_name = "2023-05-04/2023-04-27T06:17:27/DDC_Polling_Boundaries.shp"
    districts_filetype = "shp"
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        code = record[0].strip()
        address = f"{record[1].strip()}, {record[3].strip()}"
        if code == "PAY":
            # Addresses in this ward are split between stations by address, not sub-district
            # Therefore we can't tell where they should vote
            return None
        return {
            "internal_council_id": code,
            "polling_district_id": code,
            "address": address,
            "postcode": "",
        }

    def district_record_to_dict(self, record):
        code = record[0].strip()
        ward = record[7].strip()
        if code == "PAY":
            # Addresses in this ward are split between stations by address, not sub-district
            # Therefore we can't tell where they should vote
            return None
        return {
            "internal_council_id": code,
            "name": f"{ward} - {code}",
            "polling_station_id": code,
        }
