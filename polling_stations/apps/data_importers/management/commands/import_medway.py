from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MDW"
    addresses_name = "2023-05-04/2023-03-29T08:36:18.336726/Eros_SQL_Output007.csv"
    stations_name = "2023-05-04/2023-03-29T08:36:18.336726/Eros_SQL_Output007.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "ME8 8DB",
            "ME8 8QQ",
            # Look wrong
            "ME2 3TG",
        ]:
            return None

        return super().address_record_to_dict(record)
