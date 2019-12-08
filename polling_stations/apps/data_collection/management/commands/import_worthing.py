from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000229"
    addresses_name = "parl.2019-12-12/Version 1/merged.tsv"
    stations_name = "parl.2019-12-12/Version 1/merged.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # user error report #205
        # Richmond Room (adj. to Assembly Hall)
        if record.polling_place_id == "1837":
            rec["location"] = Point(-0.372557, 50.814974, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline6 in ["BN11 2FL", "BN11 2FJ", "BN11 1BF"]:
            rec["accept_suggestion"] = False

        return rec
