from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000042"
    addresses_name = "2020-02-24T14:42:16.809943/Democracy_Club__07May2020.tsv"
    stations_name = "2020-02-24T14:42:16.809943/Democracy_Club__07May2020.tsv"
    elections = ["2020-05-07"]
    csv_delimiter = "\t"

    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # Chawleigh Jubilee Hall
        if record.polling_place_id == "8295":
            rec["location"] = Point(-3.83293, 50.89860, srid=4326)

        # Oakford Village Hall
        if record.polling_place_id == "8403":
            rec["location"] = Point(-3.550351, 50.982061, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline6 in [
            "EX16 8RA",
            "EX16 7RW",
            "EX17 3QQ",
            "EX5 4LA",
            "EX16 9BQ",
            "EX16 8NW",
        ]:
            return None

        return rec
