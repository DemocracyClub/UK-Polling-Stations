from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SWL"
    addresses_name = "2024-07-04/2024-06-25T08:59:58.688923/Eros_SQL_Output003 (9).csv"
    stations_name = "2024-07-04/2024-06-25T08:59:58.688923/Eros_SQL_Output003 (9).csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if record.housepostcode in [
            # split
            "ME10 2EF",
            "ME12 2SG",
            "ME12 1TF",
            "ME10 3TU",
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
            "10093084893",  # 3 HOUSSON AVENUE, SITTINGBOURNE
            "10093084895",  # 5 HOUSSON AVENUE, SITTINGBOURNE
            "10093084891",  # 1 HOUSSON AVENUE, SITTINGBOURNE
        ]:
            return None

        return super().address_record_to_dict(record)
