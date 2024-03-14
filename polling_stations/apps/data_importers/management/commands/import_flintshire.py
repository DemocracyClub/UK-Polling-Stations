from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FLN"
    addresses_name = (
        "2024-05-02/2024-03-14T09:23:24.751789/Democracy_Club__02May2024 (16).tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-14T09:23:24.751789/Democracy_Club__02May2024 (16).tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        #  Village Hall/Neuadd Y Pentref, Pantymwyn CH7 3EH
        if record.polling_place_id == "7221":
            record = record._replace(polling_place_postcode="CH7 5EH")

        #  Address: Community Centre/Canolfan Gymunedol, Cymau, Nr. Wrexham/Nr. Wrecsam LL11 5EN
        if record.polling_place_id == "7276":
            record = record._replace(polling_place_postcode="LL11 5EU")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013716442",  # TY NANT BARN, WHITFORD ROAD, WHITFORD, HOLYWELL
            "10013704303",  # NANT Y BI, DOWNING ROAD, WHITFORD, HOLYWELL
            "10013706023",  # BRYN CADW, LLWYN IFOR LANE, WHITFORD, HOLYWELL
            "10093282336",  # BRYN CADW (2) ACCESS ROAD TO CAE COCH FARM, WHITFORD
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
        ]:
            return None
        if record.addressline6 in [
            # split
            "CH7 2JR",
            "CH4 0PE",
            "CH5 1PD",
            "CH5 1QR",
            "CH8 7ED",
            "CH7 3DG",
            "CH8 8LR",
            "CH7 6YX",
            "CH7 2JP",
            "CH7 6BA",
            "CH8 8JY",
            "CH5 3EF",
            "CH7 6TH",
            "CH7 6EH",
            "CH7 6SD",
            "LL12 9HN",
            "CH6 5TP",
            "CH8 8NF",
            "CH7 6PA",
            "CH8 9NY",
            "CH8 8NY",
            "LL12 9DU",
            "CH7 6AH",
            "CH8 7PQ",
            # suspect
            "CH8 7AX",
            "CH8 7LS",
            "CH8 7LY",
            "CH8 7EY",
            "CH6 6ES",
            "CH5 4XL",
        ]:
            return None
        return super().address_record_to_dict(record)
