from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SDE"
    addresses_name = (
        "2025-05-01/2025-03-17T11:27:30.293396/Democracy_Club__01May2025 (2).tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-17T11:27:30.293396/Democracy_Club__01May2025 (2).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10091583505",  # LONG MEADOW, GRANGEWOOD, NETHERSEAL, SWADLINCOTE
                "10091583496",  # SALT COTTAGE HEATH LANE, BOUNDARY, SWADLINCOTE
                "10091581856",  # 49 ASHBY ROAD, WOODVILLE, SWADLINCOTE
                "10091581857",  # 51 ASHBY ROAD, WOODVILLE, SWADLINCOTE
                "200001489411",  # STABLE LODGE, TWYFORD ROAD, BARROW-ON-TRENT, DERBY
                "100032026593",  # WATERWORKS HOUSE, DERBY ROAD, STANTON-BY-BRIDGE, DERBY
                "100030238970",  # 1 MARSTON LANE, HATTON, DERBY
                "100030231955",  # 2 NEWTON MOUNT COTTAGES, BRETBY LANE, BRETBY, BURTON-ON-TRENT
                "100032244975",  # WEBB COURT, PARK ROAD, OVERSEAL, SWADLINCOTE
                "10000820723",  # SALTERSFORD HOUSE, EGGINTON, DERBY
                "200003154106",  # BIRCHTREES FARM, EGGINTON, DERBY
                "10094713650",  # 46 SWARTLING DRIVE, WOODVILLE, SWADLINCOTE
                "10024227070",  # 8 BURTON ROAD, OVERSEAL, SWADLINCOTE
                "10013902860",  # FLAT 222 RYKNELD ROAD, FINDERN, DERBY
                "200003148307",  # ROYDON HALL COTTAGE CANAL BANK, SHARDLOW, DERBY
                "100030233812",  # BROADSTONE, BROADSTONE LANE, TICKNALL, DERBY
                "100030233814",  # STAUNTON VIEW, BROADSTONE LANE, TICKNALL, DERBY
                "100030233813",  # BROAD STONE END, BROADSTONE LANE, TICKNALL, DERBY
                "10023236230",  # 211 ASHBY ROAD, WOODVILLE, SWADLINCOTE
                "100030244640",  # 207 ASHBY ROAD, WOODVILLE, SWADLINCOTE
                "100032000594",  # 483 BURTON ROAD, MIDWAY, SWADLINCOTE
                "10094715060",  # 194 HIGH STREET, NEWHALL, SWADLINCOTE
                "10094715065",  # 204 HIGH STREET, NEWHALL, SWADLINCOTE
                "100030232079",  # 213 BRETBY LANE, BRETBY, BURTON-ON-TRENT
                "100030232080",  # 215 BRETBY LANE, BRETBY, BURTON-ON-TRENT
                "10090304354",  # PLOT 7 CASTLE VIEW UTTOXETER ROAD, FOSTON, DERBY
                "10090304393",  # PLOT 10 CASTLE VIEW UTTOXETER ROAD, FOSTON, Derby
                "10090303646",  # PLOT 3 CASTLE VIEW UTTOXETER ROAD, FOSTON, Derby
                "10090303645",  # PLOT 6 CASTLE VIEW UTTOXETER ROAD, FOSTON, Derby
                "100030235122",  # FOSTON MILL FARM, MILL LANE, CHURCH BROUGHTON, DERBY
                "100030234148",  # THATCHED COTTAGE, CASTLE STREET, MELBOURNE, DERBY
                "10094715625",  # 20 FIELD VIEW, WOODVILLE, SWADLINCOTE
                "10090303714",  # WOODEN BUNGALOW DERBY ROAD, MELBOURNE, DERBY
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "DE65 6LE",
            "DE65 5FH",
            "DE11 7NB",
            # looks wrong
            "DE11 9NT",
            "DE6 5JF",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Ignore warning: Polling station Mobile Unit (10440) is in Derby City Council (DER)
        # Polling station have correct location, just outside the council border

        # Location correction for: Michael`s Church - Sutton on the Hill, Church Lane, Sutton-on-the-Hill, Derby
        if record.polling_place_id == "10474":
            record = record._replace(
                polling_place_easting="423745",
                polling_place_northing="334238",
            )
        return super().station_record_to_dict(record)
