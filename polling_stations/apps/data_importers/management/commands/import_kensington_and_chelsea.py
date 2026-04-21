from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KEC"
    addresses_name = (
        "2026-05-07/2026-03-23T15:39:45.538368/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-23T15:39:45.538368/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        # bugreport # 779
        # remove suspect coords for:
        # St Philip`s Church, Earl`s Court Road, London, W8 6QH
        if record.polling_place_id == "1610":
            record = record._replace(
                polling_place_easting="0",
                polling_place_northing="0",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "SW1X 0HX",
            "W11 4HD",
            "W11 4JJ",
        ]:
            return None

        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "217016105",  # 4 CLAREVILLE GROVE, LONDON
            "217091450",  # 208A WESTBOURNE GROVE, LONDON
        ]:
            return None

        return super().address_record_to_dict(record)
