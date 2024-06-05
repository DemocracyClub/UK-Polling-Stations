from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WLN"
    addresses_name = "2024-07-04/2024-06-05T12:19:11.685198/Eros_SQL_Output003.csv"
    stations_name = "2024-07-04/2024-06-05T12:19:11.685198/Eros_SQL_Output003.csv"
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.housepostcode.replace("\xa0", " ") in [
            # split
            "EH49 6BQ",
            "EH48 2GT",
            "EH47 7NL",
            "EH52 6PP",
            "EH52 6FU",
            "EH49 6BD",
        ]:
            return None
        return super().address_record_to_dict(record)
