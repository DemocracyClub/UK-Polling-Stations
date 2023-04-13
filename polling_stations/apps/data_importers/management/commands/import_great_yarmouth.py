from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GRY"
    addresses_name = "2023-05-04/2023-04-13T15:17:40.056177/Eros_SQL_Output002.csv"
    stations_name = "2023-05-04/2023-04-13T15:17:40.056177/Eros_SQL_Output002.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "NR29 4SL",
            "NR31 8AR",
            "NR31 9JF",
            "NR31 9NY",
            "NR31 9UP",
            "NR30 5JU",
            "NR31 9EJ",
            "NR31 9PN",
            "NR30 2DR",
            "NR30 2PY",
            "NR31 0AZ",
            "NR30 2DU",
            "NR31 9TY",
            "NR31 6SY",
            # look wrong
            "NR31 9AQ",
            "NR29 3DJ",
            "NR31 8DH",
        ]:
            return None

        return super().address_record_to_dict(record)
