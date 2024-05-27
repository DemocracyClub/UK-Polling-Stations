from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHN"
    addresses_name = (
        "2024-07-04/2024-05-27T21:11:46.157637/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-27T21:11:46.157637/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "39097215",  # 8 PARK AVENUE NORTH, NEWTON-LE-WILLOWS
            "39053135",  # ROOM 5, COHAB HOUSE, 19 SHAW STREET, ST. HELENS
        ]:
            return None
        if record.addressline6 in [
            # split
            "WA10 1HT",
            "WA9 3RR",
        ]:
            return None

        return super().address_record_to_dict(record)
