from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SKE"
    addresses_name = "2024-07-04/2024-05-30T09:16:42.120699/SKE_combined.tsv"
    stations_name = "2024-07-04/2024-05-30T09:16:42.120699/SKE_combined.tsv"
    elections = ["2024-07-04"]
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
            "NG32 1AT",
            "NG31 9JZ",
            "NG32 2LW",
            "PE10 9RP",
            "NG33 4JQ",
            # suspect
            "NG31 8NH",  # MANTHORPE, GRANTHAM
            "PE10 9NG",  # BURGHLEY STREET, BOURNE
            "PE6 9QB",  # LANGTOFT LAKES
        ]:
            return None

        return super().address_record_to_dict(record)
