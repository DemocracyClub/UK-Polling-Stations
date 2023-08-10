from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BAE"
    addresses_name = (
        "2023-05-04/2023-03-17T15:33:20.577893/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-17T15:33:20.577893/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "S80 2DS",
            "S81 7HT",
            "DN22 8AH",
            "S80 1QU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.polling_place_id == "12602":  # Carlton Youth Centre
            record = record._replace(polling_place_postcode="")
        if record.polling_place_id == "12331":  # Lound Village Hall
            record = record._replace(polling_place_postcode="DN22 8RX")
        if record.polling_place_id == "12328":  # Barnby Moor Village Hall
            record = record._replace(polling_place_postcode="DN22 8QU")
        if record.polling_place_id == "12560":  # The Butter Market
            record = record._replace(polling_place_postcode="DN22 6DB")
        if record.polling_place_id == "12527":  # Langold Village Hall - Committee Room
            record = record._replace(polling_place_postcode="S81 9SW")
        if record.polling_place_id == "12392":  # Harworth & Bircotes Town Hall
            record = record._replace(polling_place_postcode="DN11 8JP")

        rec = super().station_record_to_dict(record)
        # Manton Parish Hall - correction brought forward from locals.
        if record.polling_place_id == "12284":
            rec["location"] = Point(-1.1105063, 53.2957291, srid=4326)

        return rec
