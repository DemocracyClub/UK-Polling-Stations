from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYC"
    addresses_name = (
        "2024-05-02/2024-04-12T10:41:41.223808/Democracy_Club__02May2024v2.tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-12T10:41:41.223808/Democracy_Club__02May2024v2.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # bugreport #645
        # coords correction for: Droitwich Spa Community (Main) Hall, Heritage Way, DROITWICH SPA, WR9 8RF
        if record.polling_place_id == "8042":
            record = record._replace(
                polling_place_easting="389734",
                polling_place_northing="263143",
            )

        # user issue report #197
        # Northwick Arms Hotel (Monroe Suite), Waterside, Evesham
        if record.polling_place_id == "7982":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.942675, 52.090313, srid=4326)
            return rec
        # Coord correction to fix map for council:

        if record.polling_place_id == "8205":
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
            "10013939808",  # COMPOST CORNER, KNOWLE HILL, EVESHAM
            "100121281842",  # PRIORY REST HOME, CRUTCH LANE, ELMBRIDGE, DROITWICH
            "100120708134",  # HALCYON, HANBURY ROAD, DROITWICH
        ]:
            return None

        if record.addressline6 in [
            # split
            "WR11 7UQ",
            "WR11 8PZ",
            "WR10 3HG",
            "WR9 7TD",
            "WR7 4PB",
        ]:
            return None

        return super().address_record_to_dict(record)
