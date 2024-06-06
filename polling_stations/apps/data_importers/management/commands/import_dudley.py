from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DUD"
    addresses_name = (
        "2024-07-04/2024-06-06T10:13:23.366029/Democracy_Club__04July2024 (21).tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-06T10:13:23.366029/Democracy_Club__04July2024 (21).tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "90159047",  # THE JAYS, HYPERION ROAD, STOURTON, STOURBRIDGE
            "90153608",  # NEW BROMLEY FARM, BROMLEY LANE, KINGSWINFORD
            "90135708",  # 106B STOURBRIDGE ROAD, DUDLEY
            "90142681",  # 106C STOURBRIDGE ROAD, DUDLEY
            "90163097",  # 50 WOLVERHAMPTON STREET, DUDLEY
            "90163098",  # 51 WOLVERHAMPTON STREET, DUDLEY
            "90163100",  # 52 WOLVERHAMPTON STREET, DUDLEY
            "90147692",  # SCHOOL HOUSE, COTWALL END ROAD, DUDLEY
            "90202527",  # LIVING ACCOMMODATION HINDU CULTURAL CENTRE 57-59 KING STREET, DUDLEY
            "100071072854",  # 59 NEW STREET, SHELFIELD, WALSALL
            "100071072810",  # 9A NEW STREET, SHELFIELD, WALSALL
            "10090903310",  # FLAT 1 73 STAFFORD STREET, WILLENHALL
            "200002877500",  # 43A HIGH STREET, BROWNHILLS, WALSALL
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
            "90091991",  # 2 HINBROOK ROAD, DUDLEY
            "90109211",  # 31 NETHERBY ROAD, DUDLEY
            "90109229",  # 66 NETHERBY ROAD, DUDLEY
            "90157092",  # 74 HAYES LANE, STOURBRIDGE
        ]:
            return None

        if record.addressline6 in [
            # splits
            "DY1 4AN",
            "B63 4BN",
            "DY1 3EP",
            "DY1 3QY",
            "DY6 7LT",
            # looks wrong
            "DY8 4LU",
            "DY2 8QB",
            "DY8 3TH",
        ]:
            return None

        return super().address_record_to_dict(record)
