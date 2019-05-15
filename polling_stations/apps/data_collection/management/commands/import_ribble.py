from data_collection.base_importers import BaseShpStationsShpDistrictsImporter


class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = "E07000124"
    elections = ["europarl.2019-05-23"]
    districts_name = (
        "local.2019-05-02/Version 1/RVBC - Polling Districts/RVBC - Polling Districts"
    )
    stations_name = (
        "local.2019-05-02/Version 1/RVBC - Polling Stations/RVBC - Polling Stations"
    )

    def district_record_to_dict(self, record):
        return {"internal_council_id": record[0], "name": record[1]}

    def station_record_to_dict(self, record):
        stations = []

        name = record[0].strip()
        address = record[1].strip()
        postcode = record[2].strip()

        district_codes = [record[3].strip(), record[4].strip(), record[5].strip()]
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
