from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SDE"
    addresses_name = (
        "2024-07-04/2024-05-29T11:57:54.622014/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-29T11:57:54.622014/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
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
            "200003152322",  # MUSE LANE FARM, MUSE LANE, BOYLESTONE, ASHBOURNE
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
        ]:
            return None

        if record.addressline6 in [
            # splits
            "DE65 6LE",
            "DE11 9HA",
            "DE11 0DQ",
            # looks wrong
            "DE11 7FL",
            "DE11 9NT",
            "DE6 5JF",
            "DE3 0AX",
            # reported to council, they will review after the elections in May '24
            "DE73 8JA",
            "DE24 5BL",
            "DE24 5BB",
            "DE24 5AR",
            "DE24 5BL",
            "DE24 5AW",
        ]:
            return None

        return super().address_record_to_dict(record)
