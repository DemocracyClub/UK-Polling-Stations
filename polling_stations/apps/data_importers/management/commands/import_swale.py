from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SWL"
    addresses_name = "2025-05-01/2025-03-11T12:31:18.335513/Eros_SQL_Output002.csv"
    stations_name = "2025-05-01/2025-03-11T12:31:18.335513/Eros_SQL_Output002.csv"
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if record.housepostcode in [
            # split
            "ME10 3TU",
            "ME12 1TF",
            "ME10 2EF",
            "ME12 2SG",
            # suspect
            "ME12 1RW",
            "ME12 1RN",
        ]:
            return None

        if uprn in [
            "200002533735",  # POPPINGTON BUNGALOW, WHITE HILL, SELLING, FAVERSHAM
            "100061091546",  # 31 HAMBROOK WALK, SITTINGBOURNE
            "100061091542",  # 27 HAMBROOK WALK, SITTINGBOURNE
            "100061091544",  # 29 HAMBROOK WALK, SITTINGBOURNE
            "100061091540",  # 25 HAMBROOK WALK, SITTINGBOURNE
        ]:
            return None

        return super().address_record_to_dict(record)
