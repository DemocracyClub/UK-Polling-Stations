from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000047"
    council_name = "Fife"
    elections = ["europarl.2019-05-23"]

    def district_record_to_dict(self, record):
        if record[0].startswith("999ZZ"):  # Fife reservoirs
            return None
        rec = super().district_record_to_dict(record)
        return rec
