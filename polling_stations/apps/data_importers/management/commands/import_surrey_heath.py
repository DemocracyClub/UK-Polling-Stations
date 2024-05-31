from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SUR"
    addresses_name = (
        "2024-07-04/2024-05-31T17:03:52.755265/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-31T17:03:52.755265/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002673659",  # THE BARN, SCOTTS GROVE ROAD, CHOBHAM, WOKING
            "10002683262",  # CARAVAN 82 GUILDFORD ROAD, BAGSHOT
            "10002683024",  # 82 GUILDFORD ROAD, BAGSHOT
            "100061549494",  # FRIMLEY LODGE, GUILDFORD ROAD, FRIMLEY GREEN, CAMBERLEY
            "10002685033",  # CORNERWAYS FRIMLEY ROAD, FRIMLEY, CAMBERLEY
            "10002685261",  # ANNEXE 5 THE GROVE, FRIMLEY, CAMBERLEY
        ]:
            return None

        if record.addressline6 in [
            # split
            "GU19 5ES",
            "GU18 5QY",
            "GU15 3RD",
            "GU15 3EH",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)
        # Heatherside Community Centre, Martindale Avenue, Camberley, Surrey, GU15 1BB
        if rec["internal_council_id"] == "2987":
            rec["location"] = Point(-0.702364, 51.329003, srid=4326)

        return rec
