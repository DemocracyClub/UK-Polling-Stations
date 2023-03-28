from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SUR"
    addresses_name = (
        "2023-05-04/2023-03-28T10:19:10.360312/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-28T10:19:10.360312/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002673659",  # THE BARN, SCOTTS GROVE ROAD, CHOBHAM, WOKING
            "10002683262",  # CARAVAN 82 GUILDFORD ROAD, BAGSHOT
            "10002683024",  # 82 GUILDFORD ROAD, BAGSHOT
            "100061549494",  # FRIMLEY LODGE, GUILDFORD ROAD, FRIMLEY GREEN, CAMBERLEY
            "100062328000",  # WITWOOD, PARK STREET, CAMBERLEY
            "200001494828",  # ARMY TRAINING ESTATES, DERA THE MAULTWAY, CAMBERLEY
            "10002684465",  # FLAT THE FROG MINDENHURST ROAD, DEEPCUT, CAMBERLEY
            "100061546252",  # CRABTREE CORNER, CRABTREE ROAD, CAMBERLEY
            "10002672927",  # THE OAKS, WHITMOOR ROAD, BAGSHOT
        ]:
            return None

        if record.addressline6 in [
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
        if rec["internal_council_id"] == "2746":
            rec["location"] = Point(-0.702364, 51.329003, srid=4326)

        return rec
