from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000021"
    council_name = "North Ayrshire"
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
            return stations
        return rec
