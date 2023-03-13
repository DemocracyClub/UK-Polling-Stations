from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "DAR"
    addresses_name = "2023-05-04/2023-03-13T13:53:29.216498/Eros_SQL_Output003.csv"
    stations_name = "2023-05-04/2023-03-13T13:53:29.216498/Eros_SQL_Output003.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # Split
            "DA10 1FB",
        ]:
            return None

        return super().address_record_to_dict(record)
