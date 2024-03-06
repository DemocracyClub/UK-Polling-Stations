from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "LIC"
    addresses_name = "2024-05-02/2024-03-06T13:47:47.801119/Eros_SQL_Output012.csv"
    stations_name = "2024-05-02/2024-03-06T13:47:47.801119/Eros_SQL_Output012.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "LN2 5HZ",
            "LN2 4NA",
            "LN5 8AG",
            "LN6 7UY",
            "LN1 1BU",
            "LN6 0LH",
            "LN2 4DY",
            "LN6 8AZ",
            "LN1 1QD",
            "LN5 7LA",
            "LN2 5EJ",
            "LN1 1DR",
            "LN6 8DB",
            "LN1 1XE",
        ]:
            return None

        return super().address_record_to_dict(record)
