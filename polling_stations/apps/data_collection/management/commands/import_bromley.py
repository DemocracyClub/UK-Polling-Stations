from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000006"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019brom.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019brom.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if record.polling_place_id == "9036":
            rec["location"] = Point(-0.058087, 51.403252, srid=4326)

        return rec

    def address_record_to_dict(self, record):

        if record.addressline6 == "BR7 6HL":
            return None

        return super().address_record_to_dict(record)
