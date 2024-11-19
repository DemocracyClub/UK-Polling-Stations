from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHN"
    addresses_name = (
        "2024-12-12/2024-11-19T11:02:39.999329/Democracy_Club__12December2024.tsv"
    )
    stations_name = (
        "2024-12-12/2024-11-19T11:02:39.999329/Democracy_Club__12December2024.tsv"
    )
    elections = ["2024-12-12"]
    csv_delimiter = "\t"

    # Maintaining GE exclusions for future reference

    # def address_record_to_dict(self, record):
    #     uprn = record.property_urn.strip().lstrip("0")

    # if uprn in [
    #     "39097215",  # 8 PARK AVENUE NORTH, NEWTON-LE-WILLOWS
    #     "39053135",  # ROOM 5, COHAB HOUSE, 19 SHAW STREET, ST. HELENS
    # ]:
    #     return None
    # if record.addressline6 in [
    #     # split
    #     "WA10 1HT",
    #     "WA9 3RR",
    # ]:
    #     return None

    # return super().address_record_to_dict(record)
