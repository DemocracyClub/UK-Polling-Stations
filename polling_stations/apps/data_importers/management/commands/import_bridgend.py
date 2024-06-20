from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BGE"
    addresses_name = "2024-07-04/2024-06-24T18:01:04.431232/bge-combined.csv"
    stations_name = "2024-07-04/2024-06-24T18:01:04.431232/bge-combined.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "CF34 0UF",
            "CF32 8TY",
            "CF31 2DH",
            "CF31 5FD",
            "CF31 3HL",
            "CF31 1NP",
            "CF34 9SD",
            "CF35 6GD",
            "CF33 6PL",
            "CF35 6HZ",
            "CF32 0NR",
            # suspect
            "CF31 2DL",  #
        ]:
            return None

        return super().address_record_to_dict(record)
