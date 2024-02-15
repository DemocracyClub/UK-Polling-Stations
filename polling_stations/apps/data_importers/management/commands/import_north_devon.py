from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NDE"
    addresses_name = (
        "2024-05-02/2024-02-15T10:14:37.490245/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-15T10:14:37.490245/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10012114417",  # THE SHIPPEN HUISH MOOR ROAD FROM FULLINGCOTT CROSS PAST BEACON FARM, INSTOW
            "10090333929",  # UNIT 1 BABLES TENEMENT ROAD FROM BALLS CORNER TO MILL MOOR CROSS, BURRINGTON
            "10094240594",  # LAND AND BUILDINGS AT 254805 145034 LANE TO WOOLSCOTT BARTON, ILFRACOMBE
            "10012099463",  # LEE DOWN FARM, COMBE MARTIN, ILFRACOMBE
            "10012091294",  # BRINSCOTT FARMHOUSE, COMBE MARTIN, ILFRACOMBE
            "10012099767",  # HORE DOWN FARM, ILFRACOMBE
        ]:
            return None

        if record.addressline6 in [
            # split
            "EX39 4PF",
            "EX36 3DJ",
            "EX31 3XW",
            "EX36 3BT",
            "EX34 9QF",
            "EX32 0PE",
            "EX32 8BS",
            "EX32 0AP",
            "EX33 2BW",
            "EX33 2NT",
            "EX33 1HW"
        ]:
            return None

        return super().address_record_to_dict(record)
