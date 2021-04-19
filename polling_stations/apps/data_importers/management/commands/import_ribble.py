from data_importers.base_importers import BaseShpStationsShpDistrictsImporter


class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = "RIB"
    elections = ["2021-05-06"]
    districts_name = "2021-03-25T12:14:33.026795747/RVBC Polling Districts.shp"
    stations_name = "2021-03-25T12:14:33.026795747/RVBC Polling Stations 2021.shp"

    def district_record_to_dict(self, record):
        return {"internal_council_id": record[1], "name": record[2]}

    def station_record_to_dict(self, record):
        stations = []

        name = record[1].strip()
        address = record[2].strip()
        postcode = record[3].strip()

        district_codes = [record[4].strip(), record[5].strip(), record[6].strip()]
        district_codes = [code for code in district_codes if code]

        for code in district_codes:
            stations.append(
                {
                    "internal_council_id": code,
                    "address": "%s\n%s" % (name, address),
                    "postcode": postcode,
                    "polling_district_id": code,
                }
            )

        return stations
