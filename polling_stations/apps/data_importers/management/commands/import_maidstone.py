from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAI"
    addresses_name = (
        "2025-05-01/2025-04-14T16:33:41.941070/Democracy_Club__01May2025 updated.tsv"
    )
    stations_name = (
        "2025-05-01/2025-04-14T16:33:41.941070/Democracy_Club__01May2025 updated.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "ME16 8DT",
            "ME15 9RA",
            "ME15 6EL",
            "ME14 3EP",
            # suspect
            "ME18 5EF",
            "ME18 5ED",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Removing wrong coordinates for: Grange Moor Hotel, St Michaels Road, Maidstone, Kent, ME16 8BS
        if record.polling_place_id == "5424":
            record = record._replace(
                polling_place_easting="",
                polling_place_northing="",
            )
        return super().station_record_to_dict(record)
