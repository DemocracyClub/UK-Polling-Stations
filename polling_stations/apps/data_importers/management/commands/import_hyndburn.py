from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HYN"
    addresses_name = (
        "2025-05-01/2025-03-05T12:41:30.941681/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-05T12:41:30.941681/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10009967792",  # 3 HIGH STREET, ACCRINGTON
                "100012878207",  # LEG LOCK FARM, SOUGH LANE, GUIDE, BLACKBURN
                "10070894822",  # 2A HIGH STREET, RISHTON, BLACKBURN
                "10070896603",  # THE OLD STABLES BROWNSILLS, MILL LANE, GREAT HARWOOD, BLACKBURN
                "10070894060",  # 2A WATER STREET, ACCRINGTON
                "10070894668",  # HARWOOD EDGE BARN, WILPSHIRE ROAD, RISHTON, BLACKBURN
                "100012393578",  # HARWOOD EDGE FARM, WILPSHIRE ROAD, RISHTON, BLACKBURN
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "BB5 5QA",
        ]:
            return None

        return super().address_record_to_dict(record)
