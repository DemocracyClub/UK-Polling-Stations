from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "YOR"
    addresses_name = "2024-07-04/2024-06-19T16:44:21.028423/York Outer and York Central polling districts 4 July 2024.csv"
    stations_name = "2024-07-04/2024-06-19T16:44:21.028423/York Outer and York Central polling stations 4 July 2024.csv"
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "YO19 6BG",
            "YO23 2QU",
            "YO19 5LB",
            "YO10 4FR",
        ]:
            return None
        return super().address_record_to_dict(record)
