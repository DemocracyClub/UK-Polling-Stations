from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SUR"
    addresses_name = (
        "2021-04-13T11:45:57.734080/Surrey Democracy_Club__06May2021 (1).CSV"
    )
    stations_name = (
        "2021-04-13T11:45:57.734080/Surrey Democracy_Club__06May2021 (1).CSV"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        rec = super().station_record_to_dict(record)
        # From: 972106:polling_stations/apps/data_importers/management/commands/misc_fixes.py-245-
        if rec["internal_council_id"] == "2622":  # Heatherside Community Centre
            rec["location"] = Point(-0.702364, 51.329003, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002680882",  # MOBILE HOME 3 WESTCROFT PARK DEVELOPMENT SITE WINDLESHAM ROAD, CHOBHAM, WOKING
            "10002680881",  # MOBILE HOME 2 WESTCROFT PARK DEVELOPMENT SITE WINDLESHAM ROAD, CHOBHAM, WOKING
            "10002680883",  # MOBILE HOME 4 WESTCROFT PARK DEVELOPMENT SITE WINDLESHAM ROAD, CHOBHAM, WOKING
            "10002680880",  # MOBILE HOME 1 WESTCROFT PARK DEVELOPMENT SITE WINDLESHAM ROAD, CHOBHAM, WOKING
            "10002673659",  # THE BARN, SCOTTS GROVE ROAD, CHOBHAM, WOKING
            "10002683262",  # CARAVAN 82 GUILDFORD ROAD, BAGSHOT
            "10002683024",  # 82 GUILDFORD ROAD, BAGSHOT
            "100061541024",  # 80 GUILDFORD ROAD, BAGSHOT
            "100061549490",  # PINES, GUILDFORD ROAD, FRIMLEY GREEN, CAMBERLEY
            "100061549494",  # FRIMLEY LODGE, GUILDFORD ROAD, FRIMLEY GREEN, CAMBERLEY
            "100062328000",  # WITWOOD, PARK STREET, CAMBERLEY
            "200001494828",  # ARMY TRAINING ESTATES, DERA THE MAULTWAY, CAMBERLEY
        ]:
            return None

        if record.addressline6 in [
            "GU15 3EH",
            "GU15 3RD",
            "GU15 2QB",
            "GU19 5ES",
            "GU20 6HZ",
            "GU18 5QY",
        ]:
            return None

        return super().address_record_to_dict(record)
