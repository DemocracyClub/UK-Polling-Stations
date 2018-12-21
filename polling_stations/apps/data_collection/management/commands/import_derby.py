from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000015"
    addresses_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018 Derby.csv"
    stations_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018 Derby.csv"
    elections = ["local.2018-05-03"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):

        # All of the UPRN data from Derby is a bit dubious.
        # I think they might have opened the CSV in Excel and accidentally
        # 'rounded' all the UPRNs with more than N digits in them
        # For safety I'm just going to ignore them all
        record = record._replace(property_urn="")

        # given we can't rely on the UPRNs, we'll have to
        # throw the baby out with the bathwater a bit here
        bad_postcodes = [
            "DE24 3LT",
            "DE23 4AA",
            "DE23 6PA",
            "DE22 2NX",
            "DE23 6GH",
            "DE24 8BE",
            "DE24 8RF",
            "DE22 3FZ",
            "DE21 2NL",
        ]

        if record.addressline6.strip() in bad_postcodes:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)
        # better grid ref
        if rec["internal_council_id"] == "6652":
            rec["location"] = Point(-1.4980912, 52.9057198, srid=4326)
        return rec
