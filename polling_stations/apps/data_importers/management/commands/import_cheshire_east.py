from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHE"
    addresses_name = "2024-07-04/2024-06-20T10:09:10.659361/CHE_combined.tsv"
    stations_name = "2024-07-04/2024-06-20T10:09:10.659361/CHE_combined.tsv"
    elections = ["2024-07-04"]
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
            "WA16 0GU",
            "CW5 7HN",
            "CW10 0JW",
            "WA16 0GQ",
            "CW10 0HY",
            "CW10 0HD",
            "CW2 8LA",
            "CW2 5QZ",
            "CW12 4DQ",
            "SK12 1UB",
            "CW12 2NA",
            # looks wrong
            "SK9 4DD",
            "SY14 8FJ",
        ]:
            return None

        return super().address_record_to_dict(record)
