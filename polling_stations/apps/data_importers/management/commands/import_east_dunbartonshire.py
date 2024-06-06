from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "EDU"
    addresses_name = "2024-07-04/2024-06-06T10:22:02.550284/Eros_SQL_Output016.csv"
    stations_name = "2024-07-04/2024-06-06T10:22:02.550284/Eros_SQL_Output016.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "G66 7HL",
            "G66 7HE",
            "G64 3ND",
            "G64 4DQ",
            "G64 2DF",
        ]:
            return None

        return super().address_record_to_dict(record)
