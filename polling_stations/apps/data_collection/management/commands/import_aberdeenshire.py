from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000034"
    council_name = "Aberdeenshire"
    elections = ["europarl.2019-05-23"]

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)
        if record[0] == "EG1202":  # District file and Stations file disagree on station
            return None
        if record[0] == "EG1106":  # District file and Stations file disagree on station
            return None
        return rec
