from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "OLD"
    addresses_name = (
        "2026-07-30/2026-06-25T10:10:41.522051/Democracy_Club__30July2026.tsv"
    )
    stations_name = (
        "2026-07-30/2026-06-25T10:10:41.522051/Democracy_Club__30July2026.tsv"
    )
    elections = ["2026-07-30"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100011199050",  # 109 BROADWAY, ROYTON, OLDHAM
                "100011199092",  # 144 BROADWAY, ROYTON, OLDHAM
                "422000034427",  # 66 ROMAN ROAD, FAILSWORTH, MANCHESTER
                "422000061537",  # 81 OLDHAM ROAD, GRASSCROFT, OLDHAM
                "422000064639",  # 2 STONEBOTTOM BROW, DOBCROSS, OLDHAM
                "422000064640",  # 4 STONEBOTTOM BROW, DOBCROSS, OLDHAM
                "422000069004",  # 3 STATION LANE, GREENFIELD, OLDHAM
                "422000102588",  # FLAT 2 76-78 MILNROW ROAD, SHAW
                "422000102589",  # FLAT 1 76-78 MILNROW ROAD, SHAW
                "422000120408",  # VALE COTTAGE, STANDEDGE, DELPH, OLDHAM
                "422000110780",  # FLOATING LIGHT, STANDEDGE, DELPH, OLDHAM
                "422000060230",  # UPPERWOOD HOUSE, HOLMFIRTH ROAD, GREENFIELD, OLDHAM
                "422000040634",  # LITTLE LEES FARM, LEES ROAD, ASHTON-UNDER-LYNE
                "422000112307",  # THE CEMETERY HOUSE, HOLLINWOOD CEMETERY, ROMAN ROAD, OLDHAM
                "422000029132",  # 482 OLDHAM ROAD, FAILSWORTH, MANCHESTER
                "100011210750",  # 37 DERBY STREET, OLDHAM
                "100011210754",  # 41 DERBY STREET, OLDHAM
                "100011210748",  # 35 DERBY STREET, OLDHAM
                "422000071141",  # GREAVES ARMS HOTEL 13 YORKSHIRE STREET, OLDHAM
                "422000069248",  # 131 UNION STREET, OLDHAM
                "422000125981",  # 100A UNION STREET, OLDHAM
                "422000130808",  # FLAT OVER 567 CHAMBER ROAD, OLDHAM
                "422000107067",  # WHITFIELD HOUSE, WHITFIELD, SHAW, OLDHAM
                "422000109909",  # GRAINS BAR FARM, GRAINS BAR, OLDHAM
                "422000113488",  # SETT STONES, THURSTON CLOUGH ROAD, DOBCROSS, OLDHAM
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "OL2 6GN",
            "OL2 8DT",
            "OL2 8TN",
            "OL8 2NE",
            "OL8 3SF",
            "OL9 6BB",
            # looks wrong
            "OL8 3HP",
            "OL1 1TD",
            "OL1 1AP",
            "OL1 3EU",
            "OL2 8HZ",
            "OL8 3HW",
            "M35 9RG",
            "OL1 3ET",
            "OL3 7AJ",
        ]:
            return None

        return super().address_record_to_dict(record)
