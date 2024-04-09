from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STE"
    addresses_name = (
        "2024-05-02/2024-02-22T12:38:40.665753/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-22T12:38:40.665753/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "3455144295",  # 2A EGERTON ROAD, HARTSHILL, STOKE-ON-TRENT
            "3455107917",  # IVY COTTAGE, WOODPARK LANE, STOKE-ON-TRENT
            "3455010479",  # ABBEY FARM, BIRCHES HEAD ROAD, STOKE-ON-TRENT
            "3455069351",  # 152 MOORLAND ROAD, STOKE-ON-TRENT
            "3455097202",  # 676 TRENTHAM ROAD, STOKE-ON-TRENT
            "3455097203",  # 678 TRENTHAM ROAD, STOKE-ON-TRENT
            "3455082463",  # THE BUNGALOW, ST. JOSEPHS PLAYING FIELDS, HANFORD, STOKE-ON-TRENT
            "3455121942",  # BURSLEM GOLF CLUB, HIGH LANE, STOKE-ON-TRENT
            "3455137292",  # CLANWAY HOUSE, CLANWAY LANE, STOKE-ON-TRENT
            "3455058910",  # 1047 LEEK NEW ROAD, STOCKTON BROOK, STOKE-ON-TRENT
            "3455058894",  # 1009 LEEK NEW ROAD, STOCKTON BROOK, STOKE-ON-TRENT
            "3455014081",  # WILKS COTTAGE, BRINDLEY LANE, LIGHT OAKS, STOKE-ON-TRENT
            "3455014080",  # HILLSIDE BUNGALOW, BRINDLEY LANE, LIGHT OAKS, STOKE-ON-TRENT
            "3455043277",  # 115 GREASLEY ROAD, STOKE-ON-TRENT
            "3455081629",  # FLAT TOLLGATE HOTEL AND LEISURE RIP
            "3455125611",  # 102 MAGDALEN ROAD, STOKE-ON-TRENT
            "3455125610",  # OLD SCHOOL HOUSE, MAGDALEN ROAD, STOKE-ON
            "3455092315",  # A HISSEY & SON LTD, TURBINE GARAGE, STONE ROAD, STOKE-ON-TRENT
            "3455092387",  # 330 STONE ROAD, STOKE-ON-TRENT
            "3455121877",  # 1 RAILWAY COTTAGES, SIDEWAY, STOKE-ON-TRENT
            "3455121878",  # 2 RAILWAY COTTAGES, SIDEWAY, STOKE-ON-TRENT
            "3455096861",  # 147 TRENT VALLEY ROAD, STOKE-ON-TRENT
            "3455014191",  # RUPZ LTD, 110 BROAD STREET, STOKE-ON-TRENT
            "345515633",  # 290 MOORLAND ROAD, STOKE-ON-TRENT
            "3455129972",  # FLAT 1 4-6 SNEYD STREET, STOKE-ON-TRENT
            "3455088230",  # 10 SNEYD STREET, STOKE-ON-TRENT
            "3455088232",  # FLAT, 12A SNEYD STREET, STOKE-ON-TRENT
            "3455153350",  # LIVING ACCOMMODATION 694 LEEK ROAD, STOKE-ON-TRENT
            "3455092385",  # 328 STONE ROAD, STOKE-ON-TRENT
            "3455008009",  # 127 BEACONSFIELD DRIVE, STOKE-ON-TRENT
            "3455008007",  # 125 BEACONSFIELD DRIVE, STOKE-ON-TRENT
            "3455035298",  # 5 ENSTONE CLOSE, STOKE-ON-TRENT
            "3455035300",  # 9 ENSTONE CLOSE, STOKE-ON-TRENT
            "3455017354",  # BYCARS HOUSE, BYCARS ROAD, STOKE-ON-TRENT
            "3455096633",  # 1 TRANTER ROAD, STOKE-ON-TRENT
            "3455056927",  # 1 KYFFIN ROAD, STOKE-ON-TRENT
            "3455000175",  # 16 ABBEY STREET, STOKE-ON-TRENT
        ]:
            return None

        if record.addressline6 in [
            # splits
            "ST4 8ND",
            "ST3 4HU",
            "ST4 2JY",
            "ST3 5PX",
            "ST4 2LE",
            "ST3 7HT",
            "ST3 2QX",
            "ST6 7DG",
            "ST3 6DU",
            # looks wrong
            "ST3 6AU",
            "ST3 6EE",
            "ST6 2JF",
            "ST4 5EZ",
            "ST4 5AF",
            "ST3 3HE",
            "ST3 6AP",
            "ST6 6HH",
            "ST6 4RT",
            "ST4 6QY",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # more accurate point for: Penkhull Village Hall Trent Valley Road Penkhull, ST4 7LG
        if rec["internal_council_id"] == "16905":
            rec["location"] = Point(-2.196169, 52.999991, srid=4326)

        # more accurate point for: St John`s Community Church Baptist Street Burslem, ST6 3JY
        if rec["internal_council_id"] == "16830":
            rec["location"] = Point(-2.196136, 53.042620, srid=4326)

        # more accurate point for: The Cuckoo Barleston Road Stoke On Trent, ST3 3LD
        if rec["internal_council_id"] == "16948":
            rec["location"] = Point(-2.150279, 52.965307, srid=4326)

        # Station change from council:
        if record.polling_place_id == "16862":
            record = record._replace(
                polling_place_name="Wheatsheaf Hotel",
                polling_place_address_1="Sheaf Street",
                polling_place_address_2="Shelton",
                polling_place_address_3="",
                polling_place_address_4="Stoke-on-Trent",
                polling_place_postcode="ST1 4LW",
            )

        return rec
