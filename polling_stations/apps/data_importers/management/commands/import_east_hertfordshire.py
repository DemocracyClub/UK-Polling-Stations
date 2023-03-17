from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EHE"
    addresses_name = (
        "2023-05-04/2023-03-17T09:01:49.570538/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-17T09:01:49.570538/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10034624304",  # JACOB NEURO CENTRE, HIGH WYCH ROAD, SAWBRIDGEWORTH
        ]:
            return None

        if record.addressline6 in [
            # split
            "CM21 0BD",
            "CM23 3QY",
            "CM21 0HX",
            "SG12 8RB",
            "SG9 9DW",
            # look wrong
            "SG12 0XY",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Albury Village Hall
        if record.polling_place_id == "4434":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(0.094440, 51.903865, srid=4326)
            return rec

        return super().station_record_to_dict(record)
