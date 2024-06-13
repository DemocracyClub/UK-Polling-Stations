from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SKP"
    addresses_name = (
        "2024-07-04/2024-06-13T16:35:20.697123/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-13T16:35:20.697123/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094501452",  # 35A GREAVE, ROMILEY, STOCKPORT
            "10090542735",  # FLAT ABOVE 136 ACRE LANE, CHEADLE HULME, CHEADLE
            "10007621264",  # FIRST FLOOR FLAT 258B FINNEY LANE, HEALD GREEN, CHEADLE
            "10090542735",  # FLAT ABOVE 136 ACRE LANE, CHEADLE HULME, CHEADLE
            "100012786974",  # 30 BUXTON ROAD, HIGH LANE, STOCKPORT
            "100011532317",  # 2 WESTMORLAND DRIVE, STOCKPORT
            "100011449293",  # 1A ACK LANE EAST, BRAMHALL, STOCKPORT
            "100011448628",  # 29 WOODFIELD ROAD, CHEADLE HULME, CHEADLE
            "100011431085",  # 9 CHURCH ROAD, CHEADLE HULME, CHEADLE
            "100012478041",  # HIGH GROVE FARM, ST. ANNS ROAD NORTH, HEALD GREEN, CHEADLE
            "10090542752",  # FLAT GATLEY GOLF CLUB MOTCOMBE ROAD, HEALD GREEN, CHEADLE
            "100011460719",  # 42 BRANKSOME ROAD, STOCKPORT
            "100012483974",  # DUFFYS, VALE ROAD FARM, VALE ROAD, STOCKPORT
            "100011502976",  # 43 MAULDETH ROAD, STOCKPORT
            "10090543201",  # 144A BERRYCROFT LANE, ROMILEY, STOCKPORT
            "100012483229",  # CLOUGH END BUNGALOW, SANDHILL LANE, MARPLE BRIDGE, STOCKPORT
            "200000785783",  # TRON BRIDGE COTTAGE, MARPLE BRIDGE, STOCKPORT
            "10090546948",  # 24A RAMILLIES AVENUE, CHEADLE HULME, CHEADLE
            "10090543172",  # FLAT ABOVE THE CROWN INN 154 HEATON LANE, STOCKPORT
            "100011431101",  # 42A CHURCH ROAD, GATLEY, CHEADLE
            "10001147833",  # 201 EDGELEY ROAD, STOCKPORT
            "100012482785",  # YEW TREE FARM, OFFERTON ROAD, STOCKPORT
            "10090543093",  # YEW TREE FARM BARN OFFERTON ROAD, OFFERTON, STOCKPORT
            "100012482780",  # HIGH TREES, OFFERTON ROAD, STOCKPORT
            "100012483705",  # LUM HOUSE, STRINES ROAD, MARPLE, STOCKPORT
            "100012483704",  # LUM BARN, STRINES ROAD, MARPLE, STOCKPORT
        ]:
            return None

        if record.addressline6 in [
            # splits
            "SK7 3DQ",
            "SK3 9HB",
            "SK6 2BD",
            "SK4 5BS",
            "SK5 7BJ",
            "SK7 4NX",
            "SK7 1JX",
            "SK6 6LP",
            "SK7 2AA",
            "SK8 4BU",
            # looks wrong
            "SK6 7AY",
            "SK6 5NP",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # more accurate point for: St Chads Church, Church Lane, Romiley, Stockport, SK6 4AA
        if record.polling_place_id == "15100":
            record = record._replace(polling_place_easting="394124")
            record = record._replace(polling_place_northing="390681")

        return super().station_record_to_dict(record)
