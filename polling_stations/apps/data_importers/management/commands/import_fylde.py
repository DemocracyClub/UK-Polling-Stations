from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FYL"
    addresses_name = (
        "2024-05-02/2024-03-08T16:02:17.131780/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-08T16:02:17.131780/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200001880578",  # FLAT C, 55 ST. ANNES ROAD WEST, LYTHAM ST. ANNES
            "200001880577",  # FLAT B, 55 ST. ANNES ROAD WEST, LYTHAM ST. ANNES
            "100012389926",  # COPPICE FARM HOUSE, WEST MOSS LANE, LYTHAM ST. ANNES
            "200002845180",  # FLAT, 6 ST. DAVIDS ROAD SOUTH, LYTHAM ST. ANNES
            "200001697189",  # HOLLY BANK, DIVISION LANE, BLACKPOOL
            "100012618360",  # FAIRHAVEN LAKE AND GARDENS INNER PROMENADE, LYTHAM ST ANNES
            "100012753403",  # CLIFTON GRANGE FARM, BLACKPOOL ROAD, CLIFTON, PRESTON
            "100010418002",  # 112 LYTHAM ROAD, FRECKLETON, PRESTON
            "100012753615",  # 72 LYTHAM ROAD, FRECKLETON
            "100012753616",  # 74 LYTHAM ROAD, FRECKLETON
            "100010400412",  # 33D CLIFTON STREET, LYTHAM ST. ANNES
            "100010400410",  # 33B CLIFTON STREET, LYTHAM ST. ANNES
            "100012620652",  # 33A CLIFTON STREET, LYTHAM ST. ANNES
            "100012620038",  # 18C CHURCH ROAD, ST. ANNES, LYTHAM ST. ANNES
            "10023481816",  # 10 WYRE STREET, ST. ANNES, LYTHAM ST. ANNES
            "100012753789",  # 50 SEA VIEW RESIDENTIAL PARK BANK LANE, BRYNING WITH WARTON
            "10091661148",  # 21B LYTHAM ROAD, FRECKLETON, PRESTON
            "10091661257",  # THE OLD SHIPPON BACK LANE, WEETON WITH PREESE
            "100010409981",  # 43 SOUTH WARTON STREET, LYTHAM ST. ANNES
            "10023484394",  # THE OLD SAWMILL, BLACKPOOL ROAD, LYTHAM ST. ANNES
            "100010413647",  # FLAT 1-3, WOODLANDS HOUSE, 74 WOODLANDS ROAD, LYTHAM ST. ANNES
            "100010410533",  # 126 ST ANDREWS ROAD SOUTH, LYTHAM ST ANNES
            "100012390106",  # POINTER HOUSE FARM, FLEETWOOD ROAD, SINGLETON, POULTON-LE-FYLDE
        ]:
            return None

        if record.addressline6 in [
            # splits
            "PR4 1PN",
            "PR4 3AR",
            "FY8 1JU",
            "PR4 2JW",
            "FY8 2AW",
            "PR4 2RY",
            "PR4 2JN",
            "PR4 0YP",
            "PR4 3DJ",
            "FY8 2LY",
            "FY8 2BS",
            "FY8 2DS",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Below warning checked and no correction needed:
        # WARNING: Polling station Princess Alexandra House (3419) is in Blackpool Borough Council

        rec = super().station_record_to_dict(record)

        # more accurate point for: St Thomas Parish Centre, St Thomas Road, Lytham St Annes
        if rec["internal_council_id"] in ["3409", "3405"]:
            rec["location"] = Point(-3.024416, 53.747426, srid=4326)

        return rec
