from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DUD"
    addresses_name = (
        "2026-05-07/2026-03-05T11:15:58.564952/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-05T11:15:58.564952/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "90150847",  # 8 CANAL COTTAGES, NETHERTON, DUDLEY, DY2 0HA
                "90123190",  # THE OLD WHARF INN, HIGH STREET, AMBLECOTE, STOURBRIDGE, DY8 4LY
                "90115156",  # 162 TURLS HILL ROAD, BILSTON, WV14 9HH
                "90159047",  # THE JAYS, HYPERION ROAD, STOURTON, STOURBRIDGE
                "90153608",  # NEW BROMLEY FARM, BROMLEY LANE, KINGSWINFORD
                "90135708",  # 106B STOURBRIDGE ROAD, DUDLEY
                "90142681",  # 106C STOURBRIDGE ROAD, DUDLEY
                "90163097",  # 50 WOLVERHAMPTON STREET, DUDLEY
                "90163098",  # 51 WOLVERHAMPTON STREET, DUDLEY
                "90163100",  # 52 WOLVERHAMPTON STREET, DUDLEY
                "90147692",  # SCHOOL HOUSE, COTWALL END ROAD, DUDLEY
                "90150770",  # HICKMERELANDS FARM, HICKMERELANDS, DUDLEY
                "90062185",  # 58 BROOM ROAD, DUDLEY
                "90017201",  # 188 WRENS HILL ROAD, DUDLEY
                "90017194",  # 174 WRENS HILL ROAD, DUDLEY
                "90017183",  # 157 WRENS HILL ROAD, DUDLEY
                "90105501",  # 170 MEADOW ROAD, DUDLEY
                "90105477",  # 123 MEADOW ROAD, DUDLEY
                "90034692",  # 58 ST. JAMES'S ROAD, DUDLEY
                "90201217",  # 1B SMITH STREET, DUDLEY
                "90053199",  # 11 BANK STREET, STOURBRIDGE
                "90038823",  # 2 SANDFORD ROAD, DUDLEY
                "90091991",  # 2 HINBROOK ROAD, DUDLEY
                "90109211",  # 31 NETHERBY ROAD, DUDLEY
                "90109229",  # 66 NETHERBY ROAD, DUDLEY
                "90157092",  # 74 HAYES LANE, STOURBRIDGE
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "B63 4BN",
            "B63 2DY",
            "DY6 7LT",
            "DY6 9BL",
            # looks wrong
            "DY2 8QB",
            "DY8 3TH",
            "DY5 1TA",
        ]:
            return None

        return super().address_record_to_dict(record)
