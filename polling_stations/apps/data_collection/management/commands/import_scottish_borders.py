from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000026"
    council_name = "Scottish Borders"
    elections = ["parl.2019-12-12"]

    def district_record_to_dict(self, record):

        # Districts with no Station
        if record[0] in ["03I", "08E", "11E"]:
            return None

        return super().district_record_to_dict(record)

    def station_record_to_dict(self, record):

        record[0] = record[0].zfill(3)
        rec = super().station_record_to_dict(record)

        if rec and record[0] == "09C":
            rec["address"] = "ROXBURGH FORMER SCHOOL, ROXBURGH, KELSO, TD5 8LZ"
            rec["location"] = None

        return rec
