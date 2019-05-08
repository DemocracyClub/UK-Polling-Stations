from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000091"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019newforest.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019newforest.tsv"
    elections = ["local.2019-05-02", "europarl.2019-05-23"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if record.polling_place_id == "7189":
            rec["location"] = Point(-1.6600948, 50.7638635, srid=4326)

        return rec
