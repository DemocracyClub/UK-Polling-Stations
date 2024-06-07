from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ABE"
    addresses_name = (
        "2024-07-04/2024-06-07T15:39:48.734869/Eros_SQL_Output001-Aberdeen.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-07T15:39:48.734869/Eros_SQL_Output001-Aberdeen.csv"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "AB21 9BE",
            "AB12 5UQ",
            "AB21 9RN",
        ]:
            return None
        return super().address_record_to_dict(record)
