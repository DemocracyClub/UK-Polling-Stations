from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000044"
    addresses_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv"
    stations_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):

        if record.addressline6 == "PO1 5BZ":
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if rec["internal_council_id"] == "3270":
            rec["location"] = Point(-1.059545, 50.7866578, srid=4326)

        return rec
