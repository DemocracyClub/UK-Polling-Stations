from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TOB"
    addresses_name = (
        "2023-05-04/2023-03-09T14:38:36.777783/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-09T14:38:36.777783/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Paignton SNU Spiritualist Church Hall Manor Corner Torquay Road Paignton TQ3 1JB
        if record.polling_place_id == "9121":
            record = record._replace(polling_place_postcode="TQ3 2JB")

        # St Annes Hall Babbacombe Road Torquay TQ1 3UH
        if record.polling_place_id == "9157":
            record = record._replace(polling_place_postcode="")

        rec = super().station_record_to_dict(record)

        # Mobile Station at DFS Car Park Willows Retail Park Nicholson Road Torquay TQ2 7TD
        if record.polling_place_id == "9014":
            rec["location"] = Point(-3.556830, 50.488924, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100040529632",  # 16 OLD TORQUAY ROAD, PAIGNTON
            "10024003083",  # 30 SHORTON ROAD, PAIGNTON
            "100040532454",  # 28 SHORTON ROAD, PAIGNTON
        ]:
            return None

        if record.addressline6 in ["TQ1 4QZ"]:
            return None

        return super().address_record_to_dict(record)
