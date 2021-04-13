from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SLA"
    addresses_name = "2021-03-25T13:54:25.566227/South Lakeland polling_station_export-2021-03-24.csv"
    stations_name = "2021-03-25T13:54:25.566227/South Lakeland polling_station_export-2021-03-24.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        # Killington Parish Hall Killington LA6 2ND
        if (
            record.pollingstationnumber == "82"
            and record.pollingstationpostcode == "LA6 2ND"
        ):
            record = record._replace(pollingstationpostcode="")

        rec = super().station_record_to_dict(record)

        if rec["internal_council_id"] == "109-selside-memorial-hall":
            rec["location"] = Point(-2.709031, 54.398317, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10003949214",  # LANE END COTTAGE, CASTERTON, CARNFORTH
            "10093234757",  # OLD STABLES, WILLOWSWAY COUNTRY ESTATE, STAINTON, KENDAL
            "200001822436",  # BECKSIDE FARM, CROOK, KENDAL
            "100110697617",  # MOSS SIDE FARM, CROOK ROAD, STAVELEY, KENDAL
            "10003948594",  # THE LODGE, BELLMAN GROUND, BOWNESS-ON-WINDERMERE, WINDERMERE
            "10093235673",  # 51 THE PASTURES, ALLITHWAITE
            "10003955950",  # RIVERSIDE COACH HOUSE, SPARK BRIDGE, ULVERSTON
            "100110693796",  # ASH COTTAGE KIRKSTONE ROAD, AMBLESIDE
        ]:
            return None

        if record.housepostcode in [
            "LA8 8LF",
            "LA11 6SQ",
            "LA7 7EB",
            "LA7 7DG",
            "LA9 7PE",
            "LA9 7SF",
            "LA9 5ES",
            "LA23 1PE",
            "LA12 7JS",
        ]:
            return None

        return super().address_record_to_dict(record)
