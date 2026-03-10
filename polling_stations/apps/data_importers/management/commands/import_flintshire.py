from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FLN"
    addresses_name = "2026-05-07/2026-02-27T11:02:16.435939/Democracy_Club__07May2026 - Flintshire.CSV"
    stations_name = "2026-05-07/2026-02-27T11:02:16.435939/Democracy_Club__07May2026 - Flintshire.CSV"
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # The postcodes of the following stations have been confirmed by the council:

        # Village Hall/Neuadd Y Pentref, Rhesycae/Rhes-y-Cae, Nr Holywell/Nr Treffynnon, CH8 8JR
        # Community Centre/Canolfan Gymunedol, Mynydd Isa, Mold/Yr Wyddgrug, CH7 6UH

        # Postcode changes confirmed by council:
        # Village Hall/Neuadd Y Pentref, Ysceifiog, Nr Holywell/Nr Treffynnon, CH8 8NR
        if record.polling_place_id == "8249":
            record = record._replace(polling_place_postcode="CH8 8NJ")

        # Rhosesmor Village Hall, Neuadd Bentref Rhosesmor, Rhosesmor, Mold/Yr Wyddgrug, CH7 6PQ
        if record.polling_place_id == "8237":
            record = record._replace(polling_place_postcode="CH7 6WF")

        # St. Michael`s Church/Eglwys Sant Mihangel, Brynford/Brynffordd, CH8 8AD
        if record.polling_place_id == "8223":
            record = record._replace(polling_place_postcode="CH8 8LQ")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
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
            "100100209552",  # WOODVILLE, HIGH STREET, BAGILLT
            "10023843516",  # ELM HOUSE, HIGH STREET, BAGILLT
            "200002942099",  # FLAT 2 WELL STREET, HOLYWELL
        ]:
            return None
        if record.addressline6 in [
            # split
            "CH7 6BA",
            "CH8 7ED",
            "CH7 6SD",
            "CH8 7PQ",
            "CH6 5TG",
            "CH8 8NY",
            "CH4 0PE",
            "CH5 3EF",
            "CH7 2JR",
            "CH8 8NF",
            "CH8 8LR",
            "CH8 8JY",
            "CH5 1QR",
            "CH7 6YX",
            "CH6 5TP",
            "CH7 6AH",
            "LL12 9DU",
            "CH5 1PD",
            "LL12 9HN",
            "CH7 6EH",
            "CH7 6PA",
            "CH7 2JP",
            # suspect
            "CH8 7AX",
            "CH8 7EY",
            "CH6 6ES",
            "CH5 4XL",
            "CH4 0QN",
        ]:
            return None
        return super().address_record_to_dict(record)
