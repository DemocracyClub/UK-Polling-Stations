# from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000035"
    addresses_name = "2020-03-16T13:26:11.776895/Democracy_Club__07May2020.tsv"
    stations_name = "2020-03-16T13:26:11.776895/Democracy_Club__07May2020.tsv"
    elections = ["2020-05-07"]
    csv_delimiter = "\t"

    # def station_record_to_dict(self, record):
    #     rec = super().station_record_to_dict(record)

    #     # Portable building on land opposite 49 Aire Road
    #     if record.polling_place_id == "7234":
    #         rec["location"] = Point(-1.39239, 53.94110, srid=4326)

    #     # user error report #215
    #     # Guiseley AFC
    #     if record.polling_place_id == "7894":
    #         rec["location"] = None

    #     # user error report #219
    #     # All Souls Church
    #     if record.polling_place_id == "7329":
    #         rec["location"] = None

    #     return rec
