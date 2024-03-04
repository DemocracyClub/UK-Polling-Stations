from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "OLD"
    addresses_name = (
        "2024-05-02/2024-03-04T11:11:13.643147/Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-03-04T11:11:13.643147/Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100011199050",  # 109 BROADWAY, ROYTON, OLDHAM
            "100011199092",  # 144 BROADWAY, ROYTON, OLDHAM
            "100011210768",  # 83 DERBY STREET, OLDHAM
            "422000014564",  # 81 DERBY STREET, CHADDERTON, OLDHAM
            "422000014571",  # 91 DERBY STREET, CHADDERTON, OLDHAM
            "422000034427",  # 66 ROMAN ROAD, FAILSWORTH, MANCHESTER
            "422000061537",  # 81 OLDHAM ROAD, GRASSCROFT, OLDHAM
            "422000064639",  # 2 STONEBOTTOM BROW, DOBCROSS, OLDHAM
            "422000064640",  # 4 STONEBOTTOM BROW, DOBCROSS, OLDHAM
            "422000069004",  # 3 STATION LANE, GREENFIELD, OLDHAM
            "422000102588",  # FLAT 2 76-78 MILNROW ROAD, SHAW
            "422000102589",  # FLAT 1 76-78 MILNROW ROAD, SHAW
            "422000107838",  # 16 CORBETT WAY, DENSHAW, OLDHAM
            "422000120352",  # FLAT 1 THE BUNGALOW 43 GRAINS ROAD, DELPH
            "422000120353",  # FLAT 2 THE BUNGALOW 43 GRAINS ROAD, DELPH
            "422000120354",  # FLAT 3 THE BUNGALOW 43 GRAINS ROAD, DELPH
            "422000120355",  # FLAT 4 THE BUNGALOW 43 GRAINS ROAD, DELPH
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
        ]:
            return None

        if record.addressline6 in [
            # splits
            "OL8 2NE",
            "OL9 6BB",
            "OL8 3SF",
            "OL2 8DT",
            "OL2 8TN",
            # looks wrong
            "OL8 3HP",
            "OL1 1TD",
            "OL1 1SJ",
            "OL1 1AP",
            "OL1 3EU",
            "OL4 2QH",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # postcode and point correction for: Waterhead Academy Sports Campus, Counthill Road, Moorside, Oldham, OL4 2PY
        if rec["internal_council_id"] == "11047":
            rec["postcode"] = "OL4 2PZ"
            rec["location"] = Point(-2.076175, 53.556648, srid=4326)

        return rec
