from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYC"
    addresses_name = (
        "2024-05-02/2024-02-13T14:01:52.087758/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-13T14:01:52.087758/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # user issue report #197
        # Northwick Arms Hotel (Monroe Suite), Waterside, Evesham
        if record.polling_place_id == "7982":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.942675, 52.090313, srid=4326)
            return rec

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
