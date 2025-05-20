from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SLK"
    addresses_name = "2025-06-05/2025-05-20T09:21:33.949450/Eros_SQL_Output004.csv"
    stations_name = "2025-06-05/2025-05-20T09:21:33.949450/Eros_SQL_Output004.csv"
    elections = ["2025-06-05"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "G75 8HZ",
            "ML3 6UG",
            "ML12 6PP",
            "G74 4DF",
            "G72 7NT",
            "G71 7TD",
            "ML3 7QW",
            "G72 8WN",
            "G75 8JW",
            "ML10 6ET",
            "ML12 6SW",
            "G71 8DG",
            "ML11 0BG",
            "G72 8FG",
            "ML10 6FB",
            "G75 8ND",
            "G73 4AP",
            "ML11 0PG",
            "G72 7XQ",
        ]:
            return None

        return super().address_record_to_dict(record)
