from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TWH"
    addresses_name = (
        "2026-05-07/2026-02-05T12:26:43.974020/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-05T12:26:43.974020/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    # Ignore addresses at Luke House, Canton Street, which look like they're on Burdett Road
    # it's an OS issue: https://app.asana.com/1/1204880536137786/task/1206776365939224

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "6146893",  # 80B BRUCE ROAD, LONDON
            "6653815",  # ROOM 733 7A WEST INDIA DOCK ROAD, LONDON
            "6653812",  # ROOM 722 7A WEST INDIA DOCK ROAD, LONDON
            "6653816",  # ROOM 721 7A WEST INDIA DOCK ROAD, LONDON
            "6653813",  # ROOM 731 7A WEST INDIA DOCK ROAD, LONDON
            "6653814",  # ROOM 732 7A WEST INDIA DOCK ROAD, LONDON
            "6739342",  # 98 ROSEBANK GARDENS NORTH, LONDON
            "6036970",  # 7B PORTMAN PLACE, LONDON
            "6748892",  # FLAT 5, 133 BRICK LANE, LONDON
        ]:
            return None
        if record.addressline6 in [
            # suspect
            "E1 6QZ",
        ]:
            return None

        return super().address_record_to_dict(record)
