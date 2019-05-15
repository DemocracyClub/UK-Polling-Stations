from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000081"
    addresses_name = (
        "europarl.2019-05-23/Version 2/Democracy_Club__23May2019 v6glos.tsv"
    )
    stations_name = "europarl.2019-05-23/Version 2/Democracy_Club__23May2019 v6glos.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # St Paul and St Stephen Church
        if record.polling_place_id == "2663":
            record = record._replace(polling_place_postcode="GL1 5AL")
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.245029, 51.854501, srid=4326)
            return rec

        if record.polling_place_id == "2599":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.206526, 51.858234, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline1.strip() == "294 Painswick Road":
            rec["postcode"] = "GL4 5DE"

        return rec
