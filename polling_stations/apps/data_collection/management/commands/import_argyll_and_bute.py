from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000035"
    council_name = "Argyll and Bute"
    elections = ["parl.2019-12-12"]

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)
        if rec:
            codes = rec["internal_council_id"].split(",")
            stations = []
            for code in codes:
                new_rec = {
                    "internal_council_id": code.strip(),
                    "postcode": rec["postcode"],
                    "address": rec["address"],
                }

                if code == "AA89":
                    new_rec["address"] = new_rec["address"].replace("?", ",")
                stations.append(new_rec)
            return stations
        return rec
