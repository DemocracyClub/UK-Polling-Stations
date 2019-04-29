from django.contrib.gis.geos import Point
from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E07000042"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019MD.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019MD.tsv"
    elections = ["local.2019-05-02/Version 1"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "7069":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
            rec = super().station_record_to_dict(record)
            rec["location"] = None
            return rec

        if record.polling_place_id == "6943":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-3.550351, 50.982061, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10035356543"  # EX153EY -> EX153EX : The Old Oaks, Chapel Hill, Uffculme, Cullompton
        ]:
            rec["accept_suggestion"] = False

        return rec
