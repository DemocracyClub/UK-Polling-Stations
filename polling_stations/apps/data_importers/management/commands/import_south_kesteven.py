from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SKE"
    addresses_name = (
        "2023-05-04/2023-04-17T15:03:42.448696/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-17T15:03:42.448696/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10007278973",  # ANNEXE 7 HIGH STREET, CAYTHORPE
            "10007248725",  # KLONDYKE FARM BUNGALOW HARVEY CLOSE, BOURNE
            "10007276237",  # 86 THE DEEPINGS CARAVAN PARK TOWNGATE EAST, MARKET DEEPING
            "100030901687",  # 5 DYKE DROVE, BOURNE
        ]:
            return None

        if record.addressline6 in [
            # splits
            "NG32 3AU",
            "NG31 9JZ",
            "NG32 1AT",
            "NG32 2LW",
            "PE10 9RP",
            "NG31 8NH",  # MANTHORPE, GRANTHAM
            "PE10 9NG",  # BURGHLEY STREET, BOURNE
        ]:
            return None

        return super().address_record_to_dict(record)
