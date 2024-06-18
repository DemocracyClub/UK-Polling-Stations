from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "PKN"
    addresses_name = "2024-07-04/2024-06-18T10:08:11.592808/PKN_combined.csv"
    stations_name = "2024-07-04/2024-06-18T10:08:11.592808/PKN_combined.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "PH2 0BL",
            "PH11 8NF",
            "PH2 6DD",
            "PH1 2BX",
            "PH1 2RH",
            "PH10 6TD",
            "PH14 9SY",
            "PH3 1HD",
        ]:
            return None
        return super().address_record_to_dict(record)
