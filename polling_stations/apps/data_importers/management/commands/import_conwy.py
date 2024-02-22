from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CWY"
    addresses_name = (
        "2024-05-02/2024-02-22T11:44:56.994639/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-22T11:44:56.994639/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.property_urn.lstrip(" 0") in [
            "50000011090",  # THE LIGHTHOUSE, MARINE DRIVE, LLANDUDNO
            "200002948867",  # THE LILLY, WEST PARADE, LLANDUDNO
            "10094422154",  # WEST VIEW, WEST PARADE, LLANDUDNO
            "100100430017",  # 91 LLANDUDNO ROAD, PENRHYN BAY, LLANDUDNO
            "50000014355",  # DELWOOD, OLD HIGHWAY, COLWYN BAY
            "200002514853",  # SUNNYSIDE, OLD HIGHWAY, COLWYN BAY
            "100100441132",  # 20 CAMBRIA ROAD, OLD COLWYN, COLWYN BAY
            "50000005841",  # BONA HOUSE, ABERGELE ROAD, LLANDDULAS, ABERGELE
            "50000016206",  # FLAT 1 REGENT HOUSE BRIDGE STREET, ABERGELE
            "10091011054",  # FLAT 2 REGENT HOUSE BRIDGE STREET, ABERGELE
            "50000015204",  # FFORDD LAS BACH, TAN Y FRON ROAD, ABERGELE
            "10024204208",  # TY GWYN FARM TOWYN ROAD, TOWYN
            "50000015204",  # FFORDD LAS BACH, TAN Y FRON ROAD, ABERGELE
            "10035304364",  # PLAS ISAF, GROESFFORDD MARLI, ABERGELE
            "10035304439",  # RHAN HIR, BYLCHAU, DENBIGH
            "10024205763",  # TY ISA, HAFOD ELWY, BYLCHAU, DENBIGH
            "10024206079",  # HAFOTTY GELYNEN, MAERDY, CORWEN
            "10024205839",  # ALLTWEN, NANT BWLCH YR HAIARN, TREFRIW
            "10024205527",  # BUARTH FARM, ROWEN, CONWY
            "50000000886",  # PINEWOOD RIDING STABLES, SYCHNANT PASS ROAD, CONWY
            "10035042289",  # THE PADDOCKS, SYCHNANT PASS ROAD, CONWY
            "10035303297",  # PENOROS, TROFARTH, ABERGELE
            "50000016886",  # COEDTEG FARM, NANT Y GLYN ROAD, COLWYN BAY
            "10024340201",  # HEN STABL, PLAS UCHA, LLANRWST
            "100100953626",  # 7A QUEENS ROAD, OLD COLWYN, COLWYN BAY
            "50000019771",  # SIAMBRWEN, BETWS ROAD, LLANRWST
            "10035303189",  # PANT Y RHEDYN, TROFARTH, ABERGELE
            "10035303093",  # CROESENGAN UCHA, TROFARTH, ABERGELE
            "10035303086",  # FFYNNON MEIRCH, TROFARTH, ABERGELE
        ]:
            return None

        if record.addressline6 in [
            # splits
            "LL30 1YQ",
            "LL32 8HW",
            "LL30 1NT",
            "LL24 0LP",
            "LL26 0YU",
            "LL31 9EQ",
            "LL22 7DT",
            "LL21 9PH",
            "LL22 8FB",  # LON BRYN ABER, ABERGELE
            "LL30 2DB",  # TAVERNERS COURT, LLOYD STREET WEST, LLANDUDNO
            "LL30 2NR",  # ST GEORGE'S PLACE, LLANDUDNO
            "LL29 8YP",  # NEW YORK COTTAGE, GROES ROAD, COLWYN BAY
            "LL29 9AB",  # ABERGELE ROAD, OLD COLWYN, COLWYN BAY
            "LL21 0PR",  # NANT Y BLODAU, TY NANT, CORWEN
        ]:
            return None

        return super().address_record_to_dict(record)
