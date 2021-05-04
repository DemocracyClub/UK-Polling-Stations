from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GLO"
    addresses_name = "2021-05-04T14:32:57.046293/Democracy_Club__06May2021.CSV"
    stations_name = "2021-05-04T14:32:57.046293/Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        # St Paul and St Stephen Church Stroud Road Gloucester GL1 5AL
        if record.polling_place_id == "3508":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.245029, 51.854501, srid=4326)
            return rec

        # St Lawrence Church Centre 32 Church Lane Gloucester GL4 3JB
        if record.polling_place_id == "3428":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.206526, 51.858234, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10007316043",  # 70 GOOSE BAY DRIVE KINGSWAY, QUEDGELEY, GLOUCESTER
            "10007317774",  # 41 AWEBRIDGE WAY, GLOUCESTER
        ]:
            return None

        if record.addressline6 in ["GL4 6JR", "GL2 4DE"]:
            return None

        return super().address_record_to_dict(record)
