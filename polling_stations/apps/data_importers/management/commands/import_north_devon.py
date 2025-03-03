from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NDE"
    addresses_name = (
        "2025-05-01/2025-03-03T09:21:19.356610/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-03T09:21:19.356610/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10012114417",  # THE SHIPPEN HUISH MOOR ROAD FROM FULLINGCOTT CROSS PAST BEACON FARM, INSTOW
                "10090333929",  # UNIT 1 BABLES TENEMENT ROAD FROM BALLS CORNER TO MILL MOOR CROSS, BURRINGTON
                "10094240594",  # LAND AND BUILDINGS AT 254805 145034 LANE TO WOOLSCOTT BARTON, ILFRACOMBE
                "10095565929",  # HAREFIELD, NEWTON TRACEY, BARNSTAPLE
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "EX31 3XW",
            "EX33 2NT",
            "EX32 8BS",
            "EX33 2BW",
            "EX36 3BT",
            "EX33 2FJ",
            "EX32 0PE",
            "EX39 4PF",
            "EX34 9QF",
            "EX36 3DJ",
            "EX32 0AP",
        ]:
            return None

        return super().address_record_to_dict(record)
