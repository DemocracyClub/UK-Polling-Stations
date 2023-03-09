from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYC"
    addresses_name = (
        "2023-05-04/2023-03-09T16:32:09.389409/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-03-09T16:32:09.389409/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        # user issue report #197
        if record.polling_place_id == "7278":  # Northwick Hotel
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.942675, 52.090313, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "WR11 7UQ",
            "WR11 8PZ",
            "WR10 3HG",
            "WR9 7TD",
            "WR7 4PB",
        ]:
            return None

        return super().address_record_to_dict(record)
