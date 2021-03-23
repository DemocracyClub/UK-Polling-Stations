from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DAL"
    addresses_name = "2021-03-19T13:08:53.439791/darlington.gov.uk-1616156390000-.tsv"
    stations_name = "2021-03-19T13:08:53.439791/darlington.gov.uk-1616156390000-.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # The Reading Room Neasham Darlington DL2 1PH
        if record.polling_place_id == "6423":
            record = record._replace(polling_place_postcode="DL2 1QX")
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.49308179, 54.48766450, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10003083588",  # ROCK COTTAGE, PIERCEBRIDGE, DARLINGTON
            "10003083581",  # DENTON GRANGE WEST, PIERCEBRIDGE, DARLINGTON
            "10003083582",  # DENTON GRANGE WEST COTTAGE, PIERCEBRIDGE, DARLINGTON
            "10003082878",  # PRO SEW, 98 ELDON STREET, DARLINGTON
            "10013318194",  # 28A YARM ROAD, DARLINGTON
        ]:
            return None

        if record.addressline6 in ["DL2 2XX"]:
            return None

        return super().address_record_to_dict(record)
