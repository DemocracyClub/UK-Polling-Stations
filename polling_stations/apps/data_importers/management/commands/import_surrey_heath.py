from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SUR"
    addresses_name = (
        "2026-05-07/2026-03-17T15:49:04.184883/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T15:49:04.184883/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002684103",  # ANNEXE 1 DAWSMERE CLOSE, CAMBERLEY, GU15 1SH
            "10002683262",  # CARAVAN 82 GUILDFORD ROAD, BAGSHOT
            "10002683024",  # 82 GUILDFORD ROAD, BAGSHOT
        ]:
            return None

        if record.addressline6 in [
            # split
            "GU18 5QY",
            "GU19 5ES",
            "GU15 3EH",
            "GU15 3RD",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)
        # location correction for: Heatherside Community Centre, Martindale Avenue, Camberley, Surrey, GU15 1BB
        if rec["internal_council_id"] == "3179":
            rec["location"] = Point(-0.702364, 51.329003, srid=4326)

        return rec
