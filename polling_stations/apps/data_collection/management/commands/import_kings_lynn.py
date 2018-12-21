from data_collection.management.commands import BaseShpStationsShpDistrictsImporter


class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = "E07000146"
    districts_name = "parl.2017-06-08/Version 3/Polling_districts.shp"
    stations_name = "parl.2017-06-08/Version 3/Polling_Stations_June17.shp"
    elections = ["parl.2017-06-08"]

    def district_record_to_dict(self, record):
        code = str(record[2]).strip()
        return {"internal_council_id": code, "name": str(record[1]).strip()}

    def parse_string(self, text):
        try:
            return text.strip().decode("utf-8")
        except AttributeError:
            return text.strip()

    def get_address(self, record):
        address_parts = [self.parse_string(x) for x in record[2:7] if x != "NULL"]
        address = "\n".join(address_parts)
        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()
        return address

    def station_record_to_dict(self, record):
        stations = []

        codes = str(record[11]).strip()

        if codes == "NOT USED":
            return None
        codes = codes.split(" ")

        for code in codes:
            stations.append(
                {
                    "internal_council_id": code,
                    "postcode": str(record[8]).strip(),
                    "address": self.get_address(record),
                    "polling_district_id": code,
                }
            )

        return stations
