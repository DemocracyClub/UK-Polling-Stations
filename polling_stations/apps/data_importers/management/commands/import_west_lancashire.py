from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLA"
    addresses_name = (
        "2023-05-04/2023-03-29T10:35:19.420584/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-29T10:35:19.420584/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100012414533",  # MOSS VIEW, CARR MOSS LANE, HALSALL, ORMSKIRK
            "100012414529",  # CARR MOSS KENNELS, CARR MOSS LANE, HALSALL, ORMSKIRK
            "100012414181",  # ALTYS FARM, ALTYS LANE, ORMSKIRK
        ]:
            return None

        if record.addressline6 in [
            # splits
            "L40 5BE",
            "PR4 6RT",
            "PR9 8FB",
            "L40 6JA",
            "L39 8SR",
            "WN8 7XA",
            "WN6 9QE",
            "WN8 6SH",
            "WN6 9EN",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # Up Holland High School, Sandbrook Road Orrell Nr Wigan
        if rec["internal_council_id"] == "9335":
            rec["location"] = Point(-2.718887, 53.528685, srid=4326)

        # Mobile Unit Adjacent to 124-128 Beechtrees Digmoor, Skelmersdale
        if rec["internal_council_id"] == "9374":
            rec["location"] = Point(-2.762784, 53.539617, srid=4326)

        return rec
