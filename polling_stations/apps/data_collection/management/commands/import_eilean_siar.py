from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000013"
    council_name = "Eilean Siar"
    elections = ["parl.2019-12-12"]

    def station_record_to_dict(self, record):

        rec = super().station_record_to_dict(record)
        if rec:
            rec["internal_council_id"] = record[0].replace("EO", "E0")
        return rec
