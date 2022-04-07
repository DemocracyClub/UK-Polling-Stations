from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BIR"
    addresses_name = (
        "2022-05-05/2022-04-07T15:09:46.475260/polling_station_export-2022-04-07.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-07T15:09:46.475260/polling_station_export-2022-04-07.csv"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # Carried forward
        if record.pollingstationname == "St Mary and Ambrose Church Hall":
            rec["postcode"] = "B5 7RA"
            rec["location"] = Point(-1.904365, 52.458623, srid=4326)

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100071441677",  # ST. EDMUND CAMPION RC SCHOOL, SUTTON ROAD, BIRMINGHAM
            "10024448607",  # 71 PAGET ROAD, BIRMINGHAM
            "10023295371",  # 10A GROSVENOR ROAD, QUINTON, BIRMINGHAM
            "100071294188",  # HAZELWELL, PINEAPPLE ROAD, BIRMINGHAM
            "10093329674",  # 35D OLTON BOULEVARD EAST, BIRMINGHAM
            "100070549934",  # 10 LENCHS CLOSE, BIRMINGHAM
            "10023509817",
            "10090246839",
        ]:
            return None

        if record.housepostcode in [
            "B13 9UA",
            "B20 3QT",
            "B23 5AL",
            "B23 7XE",
            "B28 9QL",
            "B29 7ES",
            "B30 1TH",
            "B31 1AE",
            "B31 2AD",
            "B31 2AE",
            "B31 2FL",
            "B31 3JE",
            "B31 5BG",
            "B31 5NH",
            "B33 9QD",
            "B34 6HN",
            "B34 6NE",
            "B7 5LD",
            "B75 5NE",
            "B75 5QB",
        ]:  # Split
            return None

        if record.housepostcode in [
            "B13 9EY",
            "B32 3QY",
        ]:  # appear wrong
            return None

        return super().address_record_to_dict(record)
