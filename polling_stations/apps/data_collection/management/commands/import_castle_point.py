from django.contrib.gis.geos import Point
from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E07000069"
    addresses_name = (
        "local.2018-05-03/Version 1/Democracy_Club__03May2018 Castlepoint.tsv"
    )
    stations_name = (
        "local.2018-05-03/Version 1/Democracy_Club__03May2018 Castlepoint.tsv"
    )
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if rec["internal_council_id"] == "1799":
            rec["location"] = Point(0.605786, 51.554074, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10004937052":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "SS8 7SL"
            return rec

        return super().address_record_to_dict(record)
