from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NHE"
    addresses_name = "2021-04-08T14:05:44.688002/Democracy_Club__06May2021.CSV"
    stations_name = "2021-04-08T14:05:44.688002/Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        if record.polling_place_id == "7979":  # Studlands Rise First School
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.013935, 52.045835, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in ["SG8 5AL", "SG8 9JU", "LU2 8NH"]:
            return None

        return super().address_record_to_dict(record)
