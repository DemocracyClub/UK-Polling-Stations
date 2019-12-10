from data_collection.management.commands import BaseScotlandSpatialHubImporter


station_map = {
    "134013877": [
        "AA",
        "BA",
        "CD",
        "CE",
        "EB",
        "FA",
        "FB",
        "FC",
        "FD",
        "FE",
        "FF",
        "FG",
        "FH",
    ],
    "134010608": ["BB"],
    "134017823": ["CA", "CB", "CC"],
    "134014778": ["DA"],
    "134016678": ["DB"],
    "134015948": ["DC"],
    "134017419": ["DD"],
    "134014556": ["EA"],
    "134015074": ["EC"],
    "134014675": ["ED"],
}


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000023"
    council_name = "Orkney Islands"
    elections = ["parl.2019-12-12"]

    def station_record_to_dict(self, record):
        council_name = self.parse_string(record[2])
        if council_name != self.council_name:
            return None

        codes = station_map[self.parse_string(record[4])]
        address = self.parse_string(record[3])
        stations = []
        for code in codes:
            stations.append(
                {"internal_council_id": code, "postcode": "", "address": address}
            )
        return stations
