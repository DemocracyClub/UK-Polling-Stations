from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GRE"
    addresses_name = (
        "2026-05-07/2026-03-23T16:04:43.499962/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-23T16:04:43.499962/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.uprn.lstrip("0").strip()

        if uprn in [
            "100020975456",  # 56A HILLREACH, LONDON
        ]:
            return None

        if record.post_code in [
            # split
            "SE3 9BT",
            "SE9 2BU",
            # suspect
            "SE10 8GS",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Removing bad coordinates for:
        # Clock House Community Centre, Defiance Walk, Woolwich Dockyard, London SE18 5QL
        if record.polling_place_id == "10437":
            record = record._replace(
                polling_place_easting="0",
                polling_place_northing="0",
            )

        return super().station_record_to_dict(record)
