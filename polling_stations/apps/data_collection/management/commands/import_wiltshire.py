from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000054"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019wilt.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019wilt.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        # user issue report #126
        # Bradford on Avon Youth Development Centre
        if record.polling_place_id == "58067":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.250676, 51.341552, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (record.addressline1, record.addressline2, record.addressline3) == (
            "Hedgerow Stables",
            "Paget Road",
            "Ludgershall",
        ) and uprn == "10013826068":
            return None

        rec = super().address_record_to_dict(record)

        return rec
