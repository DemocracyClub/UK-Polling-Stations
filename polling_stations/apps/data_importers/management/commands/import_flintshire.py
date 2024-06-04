from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FLN"
    addresses_name = (
        "2024-07-04/2024-06-04T10:04:48.599321/Democracy_Club__04July2024 (18).tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-04T10:04:48.599321/Democracy_Club__04July2024 (18).tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013716442",  # TY NANT BARN, WHITFORD ROAD, WHITFORD, HOLYWELL
            "10013704303",  # NANT Y BI, DOWNING ROAD, WHITFORD, HOLYWELL
            "10013706023",  # BRYN CADW, LLWYN IFOR LANE, WHITFORD, HOLYWELL
            "10090462571",  # PLYMOUTH COPSE, BABELL, HOLYWELL
            "10013705239",  # DYFFRYN AUR, BABELL, HOLYWELL
            "10013716952",  # NANT Y FUWCH, PENTRE HALKYN, HOLYWELL
            "10013694502",  # HOLLY COTTAGE, WINDMILL, PENTRE HALKYN, HOLYWELL
            "10013694267",  # 3 MOEL VIEW, WERN ROAD, RHOSESMOR, MOLD
            "10013695024",  # 1 MOEL VIEW, WERN ROAD, RHOSESMOR, MOLD
            "10023845151",  # 2 MOEL VIEW, WERN ROAD, RHOSESMOR, MOLD
            "10013707528",  # BROOKLANDS, FFRITH, WREXHAM
            "100100930264",  # THE GRANGE, SANDY LANE, HIGHER KINNERTON, CHESTER
            "200002940307",  # GRANGE FARM COTTAGE, SANDY LANE, HIGHER KINNERTON, CHESTER
            "100100219238",  # 86 SANDY LANE, HIGHER KINNERTON, CHESTER
            "10013707814",  # OLD ORCHARD, OLD LONDON ROAD, BAGILLT
            "100100209552",  # WOODVILLE, HIGH STREET, BAGILLT
            "10023843516",  # ELM HOUSE, HIGH STREET, BAGILLT
            "200002942099",  # FLAT 2 WELL STREET, HOLYWELL
            "100100939330",  # ROCK COTTAGE, CYMAU ROAD, FFRITH, WREXHAM
        ]:
            return None
        if record.addressline6 in [
            # split
            "CH8 8NF",
            "CH4 0PE",
            "CH8 8LR",
            "CH7 6YX",
            "CH5 3EF",
            "CH5 1QR",
            "CH7 2JR",
            "CH6 5TP",
            "CH8 8NY",
            "CH5 1PD",
            "CH8 8JY",
            "CH7 6BA",
            "CH8 7ED",
            "CH8 9NY",
            "CH7 3DG",
            "CH7 6SD",
            "CH7 6PA",
            "LL12 9HN",
            "CH7 6EH",
            "CH8 7PQ",
            "CH7 6AH",
            "LL12 9DU",
            "CH7 2JP",
            "CH7 6TH",
            # suspect
            "CH8 7AX",
            "CH8 7LS",
            "CH8 7LY",
            "CH8 7EY",
            "CH6 6ES",
            "CH5 4XL",
            "CH4 0QN",
        ]:
            return None
        return super().address_record_to_dict(record)
