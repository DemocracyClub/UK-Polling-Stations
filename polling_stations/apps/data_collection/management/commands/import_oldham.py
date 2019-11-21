from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000004"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019oldham.tsv"
    )
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019oldham.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        if record.polling_place_id == "6196":
            record = record._replace(polling_place_postcode="")
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.148726, 53.514296, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6.strip() == "M35 09D":
            rec["postcode"] = "M35 0PD"

        if record.addressline2 == "185B Huddersfield Road":
            return None
        if "The Bungalow Deeside Gardens" in record.addressline1:
            return None
        if "Hill Brow Close" in record.addressline1:
            return None

        if uprn in [
            "422000129521",
            "422000120408",
            "422000118702",
            "422000120682",
            "422000120353",
            "422000129006",
            "422000112898",
            "422000118887",
            "422000069004",
            "422000126990",
            "422000119217",
            "422000061537",
            "100011199092",
            "100011199050",
            "422000118382",
        ]:
            return None

        if uprn in [
            "100012737571",  # OL35QL -> OL35AG : Ladbrook, Sandy Lane, Dobcross
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "422000111697",  # OL45SN -> OL35SP : 150 Oldham Road, Springhead
            "422000111695",  # OL45SN -> OL35SP : 146 Oldham Road, Springhead
            "422000111696",  # OL45SN -> OL35SP : 148 Oldham Road, Springhead
            "422000034208",  # M359JN -> M359JR : 69 Church Street, Failsworth
            "422000126515",  # OL43FS -> OL43QA : 1 Old Manor Farm Close, Oldham
        ]:
            rec["accept_suggestion"] = False

        return rec
