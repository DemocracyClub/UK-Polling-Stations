from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EXE"
    addresses_name = (
        "2025-05-01/2025-04-10T12:52:21.787573/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-04-10T12:52:21.787573/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10023121146",  # 210A TOPSHAM ROAD, EXETER
            "10091473295",  # EXE VIEW LODGE, STOKE HILL, EXETER
        ]:
            return None

        if record.addressline6 in [
            # split
            "EX2 7TF",
            "EX2 7AY",
            "EX4 5AJ",
            "EX4 9HE",
        ]:
            return None
        return super().address_record_to_dict(record)
