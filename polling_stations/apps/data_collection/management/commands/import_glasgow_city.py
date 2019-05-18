from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000046"
    council_name = "Glasgow City"
    elections = ["europarl.2019-05-23"]

    def district_record_to_dict(self, record):
        """
        There's been a boundary change, some datasets have caught up,
        others haven't. Conveniently the 'transfer area' from Glagow to
        North Lanarkshire corresponds neatly to polling district PR2021.
        So for now we're throwing it away.
        """
        if record[0] == "PR2021":
            return None

        return super().district_record_to_dict(record)

    def station_record_to_dict(self, record):
        """
        Throw away the polling station that corresponds to discarded
        polling district as well.
        """
        if record[0] == "PR2021":
            return None

        return super().station_record_to_dict(record)
