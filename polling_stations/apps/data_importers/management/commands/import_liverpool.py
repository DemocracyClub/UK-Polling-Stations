from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LIV"
    addresses_name = (
        "2023-05-04/2023-03-16T11:13:36.358408/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-16T11:13:36.358408/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "38159023",  # 304 WALTON LANE, LIVERPOOL
            "38159026",  # 308 WALTON LANE, LIVERPOOL
            "38085354",  # 94 KINGSHEATH AVENUE, LIVERPOOL
            "38085356",  # 96 KINGSHEATH AVENUE, LIVERPOOL
            "38085358",  # 98 KINGSHEATH AVENUE, LIVERPOOL
            "38039513",  # LITTLEWOOD LODGE, CROXTETH PARK, LIVERPOOL
        ]:
            return None

        if record.addressline6 in [
            # splits
            "L8 7HN",
            "L11 4TD",
            "L16 0JW",  # CHILDWALL ABBEY ROAD, LIVERPOOL
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Warning about Fazakerley Social Club (9961) consulted, no correction needed.

        # Palmerston Tennis Club, Rear of 42 Elm Hall Drive, L15 5HZ
        if record.polling_place_id == "10066":
            record = record._replace(polling_place_postcode="L18 5HZ")

        # Temporary Polling Station	Opposite 2 Lingfield Road, Near Its Junction With, Thomas Drive, L14
        if record.polling_place_id == "9872":
            record = record._replace(polling_place_postcode="L14 3LF")

        # Temporary Polling Station	Broadway Nursing Home, Flemington Avenue, Liverpool, L4
        if record.polling_place_id == "9915":
            record = record._replace(polling_place_postcode="L4 8UD")

        # Temporary Polling Station, Coachmans Drive, Liverpool, L12
        if record.polling_place_id == "9847":
            record = record._replace(polling_place_postcode="L12 0HX")

        rec = super().station_record_to_dict(record)

        # Longmoor Lane Social Club, Longmoor Lane, Liverpool
        if rec["internal_council_id"] == "9966":
            rec["location"] = Point(-2.943939, 53.468756, srid=4326)

        # Knotty Ash Primary School, Thomas Lane, Liverpool
        if rec["internal_council_id"] == "10026":
            rec["location"] = Point(-2.891686, 53.417275, srid=4326)

        return rec
