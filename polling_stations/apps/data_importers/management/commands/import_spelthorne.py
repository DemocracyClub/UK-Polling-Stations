from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SPE"
    addresses_name = "2023-05-04/2023-04-13T10:33:05.733273/Eros_SQL_Output009.csv"
    stations_name = "2023-05-04/2023-04-13T10:33:05.733273/Eros_SQL_Output009.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "TW15 1AG",
            "TW18 1HE",
            "TW15 3SH",
            # look wrong
            "TW17 8SY",
        ]:
            return None

        return super().address_record_to_dict(record)
