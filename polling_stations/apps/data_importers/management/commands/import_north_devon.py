from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NDE"
    addresses_name = (
        "2024-07-04/2024-05-28T16:33:08.462543/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-28T16:33:08.462543/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
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
            "EX32 0AP",
            "EX32 8BS",
            "EX39 4PF",
            "EX33 2NT",
            "EX31 3XW",
            "EX32 0PE",
            "EX33 2BW",
            "EX36 3BT",
            "EX36 3DJ",
            "EX34 9QF",
            "EX33 1HW",
        ]:
            return None

        return super().address_record_to_dict(record)
