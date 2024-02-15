from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LIV"
    addresses_name = "2024-05-02/2024-02-15T11:42:39.094891/liverpool_deduped.tsv"
    stations_name = "2024-05-02/2024-02-15T11:42:39.094891/liverpool_deduped.tsv"
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "38159023",  # 304 WALTON LANE, LIVERPOOL
            "38159026",  # 308 WALTON LANE, LIVERPOOL
            "38159021",  # 302 WALTON LANE, LIVERPOOL
            "38140298",  # 124 SMITHDOWN ROAD, LIVERPOOL
            "38117786",  # 28 PICTON ROAD, WAVERTREE, LIVERPOOL
            "38277973",  # WALTON HALL PARK LODGE, WALTON HALL AVENUE, LIVERPOOL
            "38039505",  # AINTREE LODGE, CROXTETH PARK, LIVERPOOL
        ]:
            return None

        if record.addressline6 in [
            # splits
            "L11 4TD",
            "L16 0JW",  # CHILDWALL ABBEY ROAD, LIVERPOOL
            "L9 9EN",  # LONGMOOR LANE, LIVERPOOL
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # Warning about Fazakerley Social Club (10542) consulted, no correction needed.
        # https://trello.com/c/iOOgAPjR/640-liverpool

        # Longmoor Lane Social Club, Longmoor Lane, Liverpool
        if rec["internal_council_id"] == "10561":
            rec["location"] = Point(-2.943939, 53.468756, srid=4326)

        # Knotty Ash Primary School, Thomas Lane, Liverpool
        if rec["internal_council_id"] == "10898":
            rec["location"] = Point(-2.891686, 53.417275, srid=4326)

        return rec
