from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "THR"
    addresses_name = (
        "2025-05-01/2025-03-26T14:00:22.033216/Democracy_Club__01May2025 (6).tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-26T14:00:22.033216/Democracy_Club__01May2025 (6).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    # By-election so maintaining exclusions from previous elections for future reference
    # def address_record_to_dict(self, record):
    #     uprn = record.property_urn.strip().lstrip("0")

    #     if (
    #         uprn
    #         in [
    #             "10095907154",  # 1A HIGH STREET, GRAYS
    #             "200001546102",  # LANGDON HALL FARM, OLD CHURCH HILL, LANGDON HILLS, BASILDON
    #             "100091297522",  # BENTLEY FARM, OLD CHURCH HILL, LANGDON HILLS, BASILDON
    #             "100091297871",  # HOB HILL FARM, BIGGIN LANE, GRAYS
    #             "10095908244",  # 251 BRANKSOME AVENUE, STANFORD-LE-HOPE
    #         ]
    #     ):
    #         return None

    #     if record.addressline6.strip() in [
    #         # splits
    #         "RM19 1QJ",
    #         "RM16 4RB",
    #     ]:
    #         return None  # split

    #     return super().address_record_to_dict(record)
