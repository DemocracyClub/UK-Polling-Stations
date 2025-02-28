from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SKE"
    addresses_name = (
        "2025-05-01/2025-02-28T11:55:34.407771/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-28T11:55:34.407771/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
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
