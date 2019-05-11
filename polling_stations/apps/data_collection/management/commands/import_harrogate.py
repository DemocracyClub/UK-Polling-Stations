from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000165"
    addresses_name = "europarl.2019-05-23/Version 2/Democracy_Club__23May2019harro.tsv"
    stations_name = "europarl.2019-05-23/Version 2/Democracy_Club__23May2019harro.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Samwaies Hall
        if record.polling_place_id == "11333":
            record = record._replace(polling_place_postcode="HG4 5ET")

        # Lofthouse Memorial Hall
        if record.polling_place_id == "11222":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.845862, 54.156945, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn == "100052009106":
            rec["postcode"] = "HG3 5AT"

        if record.addressline6.strip() == "YO7 4ED":
            return None

        return rec
