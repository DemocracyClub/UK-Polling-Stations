from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BRC"
    addresses_name = "2023-05-04/2023-03-30T16:50:30.358526/Eros_SQL_Output002.csv"
    stations_name = "2023-05-04/2023-03-30T16:50:30.358526/Eros_SQL_Output002.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "SL5 8RY",
            "RG42 2FB",
            "RG42 6BX",
        ]:
            return None

        return super().address_record_to_dict(record)
