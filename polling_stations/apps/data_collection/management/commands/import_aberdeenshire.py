from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000034"
    council_name = "Aberdeenshire"
    elections = ["parl.2019-12-12"]

    def district_record_to_dict(self, record):

        if record[0] in [
            "DG0102",
            "DG0110",
            "DG0205",
            "DG0103",
            "DG0101",
            "DG0202",
            "DG0106",
            "DG0207",
            "DG0208",
            "DG0203",
            "DG0201",
            "DG0206",
            "DG0107",
            "DG0105",
            "DG0204",
        ]:
            return None

        return super().district_record_to_dict(record)

    def station_record_to_dict(self, record):

        if record[0] in [
            "DG0102",
            "DG0110",
            "DG0205",
            "DG0103",
            "DG0101",
            "DG0202",
            "DG0106",
            "DG0207",
            "DG0208",
            "DG0203",
            "DG0201",
            "DG0206",
            "DG0107",
            "DG0105",
            "DG0204",
        ]:
            return None

        return super().station_record_to_dict(record)
