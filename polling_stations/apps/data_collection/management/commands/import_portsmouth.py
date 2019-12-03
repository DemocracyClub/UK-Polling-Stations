from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000044"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019port.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019port.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 == "PO4 099":
            rec["postcode"] = "PO4 0PL"

        if uprn in ["1775078308", "1775002824", "1775002823"]:
            rec = super().address_record_to_dict(record)
            rec["accept_suggestion"] = True
            return rec

        if uprn in ["1775100211", "1775125846"]:
            return None

        return rec

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # St Margaret's Parish Centre
        if rec["internal_council_id"] == "4319":
            rec["location"] = Point(-1.067090, 50.786643, srid=4326)
        # Eastney Methodist Church
        if rec["internal_council_id"] == "4331":
            rec["location"] = Point(-1.059545, 50.7866578, srid=4326)

        return rec
