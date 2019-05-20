from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000054"
    addresses_name = (
        "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Wiltshire.tsv"
    )
    stations_name = (
        "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Wiltshire.tsv"
    )
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # user issue report #126
        # Bradford on Avon Youth Development Centre
        if record.polling_place_id == "53402":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.250676, 51.341552, srid=4326)
            return rec

        return super().station_record_to_dict(record)
