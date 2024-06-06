from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHE"
    addresses_name = (
        "2024-07-04/2024-06-06T12:06:58.747543/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-06T12:06:58.747543/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100010170913",  # 10 CROSSFIELD ROAD, HANDFORTH, WILMSLOW
            "100010174333",  # AQUATICS @ WILMSLOW LTD, 145 MANCHESTER ROAD, WILMSLOW
            "10007953840",  # FOUR OAKS, THE COPPICE, POYNTON, STOCKPORT
            "100010142260",  # 149 BUXTON ROAD, MACCLESFIELD
            "100012367117",  # GOLDEN HILL FARM, WINCLE, MACCLESFIELD
        ]:
            return None

        if record.addressline6 in [
            # splits
            "SK12 1UB",
            "SK10 3PG",
            "CW12 3RF",
            "WA16 0GQ",
            "WA16 0GU",
            "CW12 2NA",
            "CW12 4DQ",
            "CW2 8LA",
            # looks wrong
            "SK9 4DD",
        ]:
            return None

        return super().address_record_to_dict(record)
