from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000042"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019MD.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019MD.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # Chawleigh Jubilee Hall
        if record.polling_place_id == "7809":
            rec["location"] = None

        # Oakford Village Hall
        if record.polling_place_id == "7949":
            rec["location"] = Point(-3.550351, 50.982061, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline6 in [
            "EX16 8RA",
            "EX16 7RW",
            "EX17 3QQ",
            "EX5 4LA",
        ]:
            return None

        return rec
