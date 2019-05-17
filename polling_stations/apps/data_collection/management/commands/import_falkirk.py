from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000014"
    council_name = "Falkirk"
    elections = ["europarl.2019-05-23"]

    def station_record_to_dict(self, record):
        # There is a code mismatch between stations and districts.
        # This matches them up.
        if record[0] == "FW507":
            record[0] = "FW506"

        rec = super().station_record_to_dict(record)

        return rec
