from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GLO"
    addresses_name = (
        "2025-05-01/2025-03-25T16:38:03.119595/Democracy_Club__01May2025_GLOUCESTER.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-25T16:38:03.119595/Democracy_Club__01May2025_GLOUCESTER.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # more accurate point for: St Paul and St Stephen Church Stroud Road Gloucester GL1 5AL
        if record.polling_place_id == "4777":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.245029, 51.854501, srid=4326)
            return rec

        # more accurate point for: St Lawrence Church Centre 32 Church Lane Gloucester GL4 3JB
        if record.polling_place_id == "15224":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.206526, 51.858234, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10007317774",  # 41 AWEBRIDGE WAY, GLOUCESTER
            "10007317846",  # FLAT, 1 LLANTHONY ROAD, GLOUCESTER
            "10007311538",  # FLAT 8 LLANTHONY ROAD, GLOUCESTER
            "200004486714",  # 24A SEYMOUR ROAD, GLOUCESTER
        ]:
            return None

        if record.addressline6 in [
            # splits
            "GL2 4TY",
            "GL4 4XU",
            "GL2 0HP",
            # looks wrong
            "GL2 5QU",
        ]:
            return None

        return super().address_record_to_dict(record)
