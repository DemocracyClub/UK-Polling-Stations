from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CLD"
    addresses_name = "2026-05-07/2026-03-17T16:40:35.655763/20260317_Democracy_Club__07May2026_CMBC.CSV"
    stations_name = "2026-05-07/2026-03-17T16:40:35.655763/20260317_Democracy_Club__07May2026_CMBC.CSV"
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # # The following are coord amendments from the council:

        # PELLON BAPTIST SUNDAY SCHOOL, SPRING HALL LANE, HALIFAX, HX1 4UA
        if record.polling_place_id == "1310":
            record = record._replace(
                polling_place_easting="407498",
                polling_place_northing="425770",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6.replace("\xa0", " ") in [
            # split
            "HX3 8FY",
            # suspect
            "HX2 0UW",
        ]:
            return None

        return super().address_record_to_dict(record)
