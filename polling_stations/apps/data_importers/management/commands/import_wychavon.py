from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYC"
    addresses_name = (
        "2025-05-01/2025-03-05T16:28:55.760571/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-05T16:28:55.760571/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # bugreport #645
        # coords correction for: Droitwich Spa Community (Main) Hall, Heritage Way, DROITWICH SPA, WR9 8RF
        if record.polling_place_id == "9361":
            record = record._replace(
                polling_place_easting="389734",
                polling_place_northing="263143",
            )

        # user issue report #197
        # Northwick Arms Hotel (Monroe Suite), Waterside, Evesham
        if record.polling_place_id == "9347":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.942675, 52.090313, srid=4326)
            return rec
        # Coord correction to fix map for council:
        # Woodland View Care Home, Woodland Way, DROITWICH SPA
        if record.polling_place_id == "9365":
            record = record._replace(
                polling_place_easting="390412",
                polling_place_northing="261303",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100120715029",  # ORCHARD COTTAGE EARLS COMMON ROAD, STOCK GREEN
            "100121276049",  # GLENFIELD HOUSE, WORCESTER ROAD, UPTON WARREN, BROMSGROVE
        ]:
            return None

        if record.addressline6 in [
            # split
            "WR11 8PZ",
            "WR9 8PR",
            "WR7 4PB",
            "WR10 3HG",
            # suspect
            "WR9 7JJ",
        ]:
            return None

        return super().address_record_to_dict(record)
