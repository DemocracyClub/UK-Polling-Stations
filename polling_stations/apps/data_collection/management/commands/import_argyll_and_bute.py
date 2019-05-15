from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000035"
    council_name = "Argyll and Bute"
    elections = ["europarl.2019-05-23"]

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
                stations.append(new_rec)

                # The following two stations have two districts voting at them.
                # There are separate codes in the district shapfile so this creates them
                if code == "AA83":
                    hunters_quay = {
                        "internal_council_id": "AA83A",
                        "postcode": rec["postcode"],
                        "address": rec["address"],
                    }
                    stations.append(hunters_quay)
                if code.strip() == "AA06":
                    bellochantuy_kilchenzie = {
                        "internal_council_id": "AA07",
                        "postcode": rec["postcode"],
                        "address": rec["address"],
                    }
                    stations.append(bellochantuy_kilchenzie)
            return stations
        return rec
