from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TWH"
    addresses_name = (
        "2024-07-04/2024-06-10T15:31:22.976107/Democracy_Club__04July2024 (14).tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-10T15:31:22.976107/Democracy_Club__04July2024 (14).tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "6141280",  # FLAT 3 28 CANNON STREET ROAD, LONDON
            "6146893",  # 80B BRUCE ROAD, LONDON
            "6141280",  # FLAT 3 28 CANNON STREET ROAD, LONDON
            "6141279",  # FLAT 2 28 CANNON STREET ROAD, LONDON
            "6141278",  # FLAT 1 28 CANNON STREET ROAD, LONDON
            "6653815",  # ROOM 733 7A WEST INDIA DOCK ROAD, LONDON
            "6653812",  # ROOM 722 7A WEST INDIA DOCK ROAD, LONDON
            "6653816",  # ROOM 721 7A WEST INDIA DOCK ROAD, LONDON
            "6653813",  # ROOM 731 7A WEST INDIA DOCK ROAD, LONDON
            "6653814",  # ROOM 732 7A WEST INDIA DOCK ROAD, LONDON
            "6739342",  # 98 ROSEBANK GARDENS NORTH, LONDON
            "6036970",  # 7B PORTMAN PLACE, LONDON
        ]:
            return None
        if record.addressline6 in [
            # suspect
            "E1 6QZ",
        ]:
            return None

        return super().address_record_to_dict(record)
