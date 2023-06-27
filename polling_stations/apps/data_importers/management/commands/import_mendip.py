from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MEN"
    addresses_name = "2023-07-20/2023-06-26T14:08:20/Eros_SQL_Output002_MEN.csv"
    stations_name = "2023-07-20/2023-06-26T14:08:20/Eros_SQL_Output002_MEN.csv"
    elections = ["2023-07-20"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "BA11 2TQ",
            "BA11 4AJ",
            "BA11 2ED",
            "BA11 5DU",
            "BA11 4SA",
            "BA11 4NY",
            "BA11 1NB",
            "BA11 2AU",
            "BA11 2XG",
            "BA11 5BT",
            "BA3 5QE",
            "BA11 5EP",
            "BA11 5HA",
            "BA4 6SY",
        ]:
            return None

        return super().address_record_to_dict(record)
