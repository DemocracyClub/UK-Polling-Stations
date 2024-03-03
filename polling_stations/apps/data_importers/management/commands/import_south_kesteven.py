from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SKE"
    addresses_name = (
        "2024-05-02/2024-03-03T16:44:19.178007/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-03T16:44:19.178007/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10007248725",  # KLONDYKE FARM BUNGALOW HARVEY CLOSE, BOURNE
            "10007276237",  # 86 THE DEEPINGS CARAVAN PARK TOWNGATE EAST, MARKET DEEPING
            "100030901687",  # 5 DYKE DROVE, BOURNE
        ]:
            return None

        if record.addressline6 in [
            # split
            "NG32 2LW",
            "NG32 1AT",
            "PE10 9RP",
            "NG31 9JZ",
            "NG33 4JQ",
            # suspect
            "NG31 8NH",  # MANTHORPE, GRANTHAM
            "PE10 9NG",  # BURGHLEY STREET, BOURNE
            "PE6 9QB",  # LANGTOFT LAKES
        ]:
            return None

        return super().address_record_to_dict(record)
