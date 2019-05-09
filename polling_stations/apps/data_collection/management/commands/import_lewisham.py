from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000023"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Lewis.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Lewis.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Sir Francis Drake Primary School
        if record.polling_place_id == "15906":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.041453, 51.485092, srid=4326)
            return rec

        # All Saints Community Centre
        if record.polling_place_id == "15955":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.048807, 51.476468, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline6.strip() == "SE10 8GA":
            return None

        return rec
