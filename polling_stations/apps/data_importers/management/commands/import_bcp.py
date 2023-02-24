from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BPC"
    addresses_name = (
        "2023-05-04/2023-02-24T09:59:47.944791/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-02-24T09:59:47.944791/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100040843225",  # 34 MOORTOWN DRIVE, WIMBORNE
            "100040763094",  # 1200 RINGWOOD ROAD, BOURNEMOUTH
            "100040742502",  # 1 HOLLOWAY AVENUE, BOURNEMOUTH
            "100040803515",  # 200 DARBYS LANE NORTH, POOLE
            "10001088278",  # THE FLAT UPTON HOUSE UPTON ROAD, POOLE
            "100040843226",  # 35 MOORTOWN DRIVE, WIMBORNE
            "10090378339",  # 2 A DORSET LAKE AVENUE, POOLE
            "10012226849",  # WOOD FARM, HOLDENHURST VILLAGE, BOURNEMOUTH
            "10094776144",  # Flat 3, 45 Richmond Park Avenue, Bournemouth, Dorset, BH8 9DN
            "10094776145",  # Flat 4, 45 Richmond Park Avenue, Bournemouth, Dorset, BH8 9DN
        ]:
            return None

        if record.addressline6 in [
            "BH17 7LG",
            "BH5 1FG",
            "BH17 0GD",
            # splits
            "BH7 6LL",
            "BH10 6BA",
            "BH6 3LF",
            "BH11 8BA",
            "BH6 3BJ",
            "BH23 3JJ",
            "BH5 1DL",
            "BH1 3EB",
            "BH6 3NH",
            "BH1 1NF",
            "BH14 0RD",
            "BH10 5JF",
            "BH12 4EB",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # Station B - St. Andrew`s Parish Centre 123, Shelbourne Road Bournemouth
        if rec["internal_council_id"] == "16194":
            rec["location"] = Point(-1.859271, 50.734333, srid=4326)

        return rec
