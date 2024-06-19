from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "EDU"
    addresses_name = "2024-07-04/2024-06-19T09:26:31.007903/EDU_combined.csv"
    stations_name = "2024-07-04/2024-06-19T09:26:31.007903/EDU_combined.csv"
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
