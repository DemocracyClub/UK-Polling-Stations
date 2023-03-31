from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FYL"
    addresses_name = (
        "2023-05-04/2023-03-27T16:54:29.854985/Democracy_Club__04May2023 (R).tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-27T16:54:29.854985/Democracy_Club__04May2023 (R).tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100010421120",  # 12 STATION ROAD, WESHAM, PRESTON
            "100010421118",  # 10 STATION ROAD, WESHAM, PRESTON
            "100010421126",  # 17 STATION ROAD, WESHAM, PRESTON
            "100010421149",  # 53 STATION ROAD, KIRKHAM
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
            "100012390106",  # POINTER HOUSE FARM, FLEETWOOD ROAD, SINGLETON, POULTON-LE-FYLDE
            "10091661257",  # THE OLD SHIPPON BACK LANE, WEETON WITH PREESE
        ]:
            return None

        if record.addressline6 in [
            # splits
            "FY8 2LY",
            "FY8 2AW",
            "PR4 1PN",
            "PR4 3DJ",
            "PR4 2JN",
            "FY8 2DS",
            "FY8 1JU",
            "PR4 2RY",
            "PR4 2JW",
            "PR4 3AR",
            "FY8 2BS",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # St Thomas Parish Centre (Function Room), St Thomas Road, Lytham St Annes
        if rec["internal_council_id"] == "3190":
            rec["location"] = Point(-3.024416, 53.747426, srid=4326)

        # St Thomas Parish Centre (The Hall), St Thomas Road, Lytham St Annes
        if rec["internal_council_id"] == "3046":
            rec["location"] = Point(-3.024416, 53.747426, srid=4326)

        return rec
