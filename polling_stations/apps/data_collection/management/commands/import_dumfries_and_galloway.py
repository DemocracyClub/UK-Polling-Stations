from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000006"
    council_name = "Dumfries and Galloway"
    elections = ["parl.2019-12-12"]

    def station_record_to_dict(self, record):

        # Corrections based on checking notice of polling place
        addresses = {
            "02J1": "COMMUNITY YOUTH CENTRE, PORT WILLIAM",
            "05F1": "TROQUEER COMMUNITY CENTRE, TROQUEER",
            "06G1": "DUMFRIES NORTH WEST CHURCH HALL",
            "08F2": "Tinwald Parish Hall",
            "12H3": "Middlebie Community Centre",
        }

        rec = super().station_record_to_dict(record)

        if rec:
            try:
                rec["address"] = addresses[rec["internal_council_id"]]
                rec["location"] = None
                return rec
            except KeyError:
                return rec

        return rec
