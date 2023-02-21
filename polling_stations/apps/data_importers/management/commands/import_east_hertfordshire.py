from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EHE"
    addresses_name = "2021-04-27T12:44:26.723598/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-27T12:44:26.723598/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "CM23 3QY",
            "CM21 0BD",
            "CM21 9BD",
            "CM21 0HX",
            "SG9 9DW",
            "SG12 8RB",
            "SG14 1LR",
            "SG14 3NE",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Albury Village Hall
        if record.polling_place_id == "3908":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(0.094440, 51.903865, srid=4326)
            return rec

        # Rhodes Arts Complex
        if record.polling_place_id == "3953":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(0.163535, 51.863442, srid=4326)
            return rec

        return super().station_record_to_dict(record)
