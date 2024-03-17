from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHE"
    addresses_name = (
        "2024-05-02/2024-03-17T11:51:25.146586/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-17T11:51:25.146586/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10014451916",  # BRINDLEY FARM, WREXHAM ROAD, BURLAND, NANTWICH
            "100010170913",  # 10 CROSSFIELD ROAD, HANDFORTH, WILMSLOW
            "100010174333",  # AQUATICS @ WILMSLOW LTD, 145 MANCHESTER ROAD, WILMSLOW
            "10007953840",  # FOUR OAKS, THE COPPICE, POYNTON, STOCKPORT
            "100010142260",  # 149 BUXTON ROAD, MACCLESFIELD
            "100012367117",  # GOLDEN HILL FARM, WINCLE, MACCLESFIELD
        ]:
            return None

        if record.addressline6 in [
            # splits
            "CW12 3RF",
            "SK10 3PG",
            "SK12 1UB",
            "WA16 0GQ",
            "CW2 5QZ",
            "WA16 0GU",
            "CW2 8LA",
            "CW5 7HN",
            "CW12 2NA",
            "CW12 4DQ",
            # looks wrong
            "SK9 4DD",
        ]:
            return None

        return super().address_record_to_dict(record)
