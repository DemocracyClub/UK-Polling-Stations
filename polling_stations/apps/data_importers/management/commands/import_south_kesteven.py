from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SKE"
    addresses_name = (
        "2025-12-11/2025-11-19T16:20:29.085210/Democracy_Club__11December2025.tsv"
    )
    stations_name = (
        "2025-12-11/2025-11-19T16:20:29.085210/Democracy_Club__11December2025.tsv"
    )
    elections = ["2025-12-11"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10007248725",  # KLONDYKE FARM BUNGALOW HARVEY CLOSE, BOURNE
        ]:
            return None

        if record.addressline6 in [
            # split
            "NG32 1AT",
            "PE10 9RP",
            "NG33 4JQ",
            # suspect
            "NG31 8NH",  # MANTHORPE, GRANTHAM
            "PE10 9NG",  # BURGHLEY STREET, BOURNE
        ]:
            return None

        return super().address_record_to_dict(record)
