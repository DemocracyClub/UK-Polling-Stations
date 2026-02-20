from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CWY"
    addresses_name = (
        "2026-05-07/2026-02-23T09:57:03.243783/Democracy_Club__07May2026 (2).tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-23T09:57:03.243783/Democracy_Club__07May2026 (2).tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.property_urn.lstrip(" 0") in [
            "50000011090",  # THE LIGHTHOUSE, MARINE DRIVE, LLANDUDNO
            "200002948867",  # THE LILLY, WEST PARADE, LLANDUDNO
            "10094422154",  # WEST VIEW, WEST PARADE, LLANDUDNO
            "100100430017",  # 91 LLANDUDNO ROAD, PENRHYN BAY, LLANDUDNO
            "100100441132",  # 20 CAMBRIA ROAD, OLD COLWYN, COLWYN BAY
            "50000016206",  # FLAT 1 REGENT HOUSE BRIDGE STREET, ABERGELE
            "10091011054",  # FLAT 2 REGENT HOUSE BRIDGE STREET, ABERGELE
            "10035304364",  # PLAS ISAF, GROESFFORDD MARLI, ABERGELE
            "10024205839",  # ALLTWEN, NANT BWLCH YR HAIARN, TREFRIW
            "10024205527",  # BUARTH FARM, ROWEN, CONWY
            "10024340201",  # HEN STABL, PLAS UCHA, LLANRWST
            "50000019771",  # SIAMBRWEN, BETWS ROAD, LLANRWST
            "10091007935",  # ABATY HEN COLWYN, ABERGELE ROAD, OLD COLWYN, COLWYN BAY
        ]:
            return None

        if record.addressline6 in [
            # splits
            "LL32 8HW",
            "LL22 7DT",
            "LL30 1YQ",
            "LL24 0LP",
            "LL30 1NT",
            "LL31 9EQ",
            "LL26 0YU",
            "LL21 9PH",
            "LL28 4AN",
            # suspect
            "LL22 8FB",
            "LL30 2DB",
            "LL34 6AQ",
        ]:
            return None

        return super().address_record_to_dict(record)
