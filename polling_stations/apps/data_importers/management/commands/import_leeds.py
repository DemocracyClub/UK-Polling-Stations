from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LDS"
    addresses_name = "2021-03-18T18:20:36.733550/leeds_deduped.tsv"
    stations_name = "2021-03-18T18:20:36.733550/leeds_deduped.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "72371873",  # SUNNYNOOK COTTAGE, PARKSIDE ROAD, LEEDS
            "72084943",  # FLAT 38 WELLINGTON STREET, LEEDS
            "72111999",  # ROOM 2 22 STRATFORD TERRACE, BEESTON, LEEDS
            "72739055",  # 54 CHURCH LANE, PUDSEY
            "72102845",  # AIREDALE CARE HOME, 56 CHURCH LANE, PUDSEY
            "72160714",  # 30 PRESTON PARADE, LEEDS
            "72288078",  # 31 PRESTON PARADE, LEEDS
            "72102848",  # MASJID IBRAHEEM, 4 WOODVIEW ROAD, LEEDS
            "72281020",  # 22 STRATFORD TERRACE, LEEDS
            "72160712",  # FLAT THE SPORTSMAN STONEY ROCK LANE, BURMANTOFTS, LEEDS
            "72501451",  # EAST COAST CONTAINERS, WOOD FARM, GELDERD ROAD, GILDERSOME, MORLEY, LEEDS
            "72686179",  # 26A STRATFORD TERRACE, BEESTON, LEEDS
            "72569600",  # 1 THE GRANGE, PARKFIELD AVENUE, LEEDS
            "72050226",  # THE GABLES, BARROWBY LANE, GARFORTH, LEEDS
            "72756557",  # 226 LEEDS ROAD, LOFTHOUSE, WAKEFIELD
            "72663962",  # 228 LEEDS ROAD, LOFTHOUSE, WAKEFIELD
            "72546421",  # SCHOOL HOUSE, KIPPAX GREENFIELD PRIMARY SCHOOL, EBOR MOUNT, KIPPAX, LEEDS
            "72733548",  # 2 THE GRANGE, PARKFIELD AVENUE, LEEDS
            "72371886",  # 1 SCHOOL BUNGALOW, LIDGETT LANE, GARFORTH, LEEDS
            "72201722",  # 60 INTAKE ROAD, PUDSEY
            "72510924",  # 111 KING LANE, LEEDS
            "72510927",  # 111 HOUGH TOP, LEEDS
            "72510928",  # 1 HOLMSLEY FIELD LANE, OULTON, LEEDS
            "72510932",  # 2 HOLMSLEY FIELD LANE, OULTON, LEEDS
            "72393521",  # 4 HOLMSLEY FIELD LANE, OULTON, LEEDS
            "72132919",  # 62 INTAKE ROAD, PUDSEY
            "72160713",  # 66 INTAKE ROAD, PUDSEY
            "72536116",  # 36A GROVE ROAD, LEEDS
            "72510933",  # THE BEECHES, WIGHILL, TADCASTER
            "72523631",  # THE OLD TACKROOM, DEAN LANE, HORSFORTH, LEEDS
            "72348012",  # 109 HOUGH TOP, LEEDS
            "72381701",  # HOLMFIELD FARM, HOLMSLEY FIELD LANE, OULTON, LEEDS
            "72288081",  # 2 TEMPLE LEA, LEEDS
            "72207662",  # 10 TEMPLE LEA, LEEDS
            "72523880",  # 6 TEMPLE LEA, LEEDS
            "72110364",  # 12 TEMPLE LEA, LEEDS
            "72207678",  # 8 TEMPLE LEA, LEEDS
            "72288080",  # 18 TEMPLE LEA, LEEDS
            "72207682",  # FLAT THE DUCK AND DRAKE INN 43 KIRKGATE, LEEDS
            "72556734",  # GREEN BANKS FARM, OTLEY OLD ROAD, LEEDS
            "72722027",  # THE OLD PIGGERY, DEAN LANE, HORSFORTH, LEEDS
            "72371889",  # THE OLD HAYBARN, DEAN LANE, HORSFORTH, LEEDS
            "72523627",  # PARK HOUSE FARM, CLAY PIT LANE, LEDSTON, CASTLEFORD
            "72085776",  # THE LAURELS, HALF MILE, LEEDS
            "72523630",  # WHITEHOUSE, OLD PARK ROAD, LEEDS
            "72739109",  # 34 BRUNTCLIFFE LANE, MORLEY, LEEDS
            "72102846",  # 29 PRESTON PARADE, LEEDS
            "72722503",  # 27 RING ROAD BEESTON PARK, LEEDS
            "72170137",  # FLAT THE REGENT 109 KIRKGATE, LEEDS
            "72560117",  # 64 INTAKE ROAD, PUDSEY
            "72523628",  # FLAT STAR INN 205 TONG ROAD, FARNLEY, LEEDS
            "72739056",  # FERNBANK, HALF MILE LANE, LEEDS
            "72569599",  # 167 MALVERN ROAD, LEEDS
            "72510925",  # 165 MALVERN ROAD, LEEDS
            "72510929",  # THE POULTRY FARM, BAY HORSE LANE, LEEDS
            "72552173",  # WAKEFIELD LIMES HOTEL, 188 LEEDS ROAD, LOFTHOUSE, WAKEFIELD
            "72324106",  # FLAT AT MORLEY UNITED SERVICES CLUB HIGH STREET, MORLEY
            "72676600",  # MAGDALENE VICTORIA ROAD, CHURWELL, MORLEY
            "72756556",  # 58 INTAKE ROAD, PUDSEY
            "72357499",  # PARK FARM COTTAGE, CLAY PIT LANE, LEDSTON, CASTLEFORD
            "72049035",  # 37 CORONATION PARADE, LEEDS
            "72090839",  # 16 TEMPLE LEA, LEEDS
            "72659064",  # 14 TEMPLE LEA, LEEDS
            "72050224",  # 22 TEMPLE LEA, LEEDS
            "72542222",  # 4 TEMPLE LEA, LEEDS
            "72527138",  # 36B GROVE ROAD, LEEDS
            "72207680",  # 30 GROVE ROAD, HEADINGLEY, LEEDS
            "72523629",  # 20 TEMPLE LEA, LEEDS
            "72281022",  # 8 COW CLOSE ROAD, LEEDS
            "72665355",  # FLAT THE PALACE KIRKGATE, LEEDS
            "72390208",  # 107 HOUGH TOP, LEEDS
            "72700401",  # 105 HOUGH TOP, LEEDS
            "72381700",  # FLAT TEMPLE NEWSAM GOLF CLUB TEMPLENEWSAM ROAD, HALTON, LEEDS
            "72510930",  # FLAT, 96 KIRKGATE, LEEDS
            "72381697",  # 54A HARROGATE ROAD, LEEDS
            "72160715",  # 1 SHAFTESBURY ROAD, LEEDS
            "72739052",  # FOX GLOVE COTTAGE, LEEDS ROAD, LOFTHOUSE, WAKEFIELD
            "72102847",  # 3 THE GRANGE, PARKFIELD AVENUE, LEEDS
            "72288079",  # 4 THE GRANGE, PARKFIELD AVENUE, LEEDS
            "72721195",  # 5 THE GRANGE, PARKFIELD AVENUE, LEEDS
            "72288076",  # 6 THE GRANGE, PARKFIELD AVENUE, LEEDS
            "72207674",  # 7 THE GRANGE, PARKFIELD AVENUE, LEEDS
            "72721594",  # 8 THE GRANGE, PARKFIELD AVENUE, LEEDS
            "72756558",  # 9 THE GRANGE, PARKFIELD AVENUE, LEEDS
            "72663302",  # 10 THE GRANGE, PARKFIELD AVENUE, LEEDS
            "72700369",  # FLAT 48 LEADWELL LANE, ROTHWELL, LEEDS
            "72510926",  # 32 PRESTON PARADE, LEEDS
            "72510931",  # 2 COW CLOSE ROAD, LEEDS
            "72050229",  # FLAT PENDAS ARMS NABURN APPROACH, WHINMOOR, LEEDS
            "72719195",  # 4 COW CLOSE ROAD, LEEDS
            "72740428",  # 46 LADY PIT LANE, LEEDS
            "72207676",  # EBOR COTTAGE, MIDDLETON ROAD, LEEDS
            "72721003",  # FLAT AT BARLEY MOW INN TOWN STREET, BRAMLEY, LEEDS
        ]:
            return None

        if record.addressline6 in [
            "LS29 6BB",
            "LS6 1PX",
            "LS17 9ED",
            "LS12 6DJ",
            "LS9 8DU",
            "LS10 2DF",
            "LS10 3TQ",
            "LS16 6FE",
            "LS21 2FF",
            "LS15 8TZ",
            "LS20 8FG",
            "LS8 2PT",
            "LS9 8LJ",
            "LS10 4AZ",
            "LS18 5HN",
            "LS3 1BT",
            "LS15 7RE",
            "LS15 0LG",
            "LS26 8AR",
            "LS26 0PB",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Bramham Village Hall (The Supper Room) Church Hill Bramham LS23 6QF
        if record.polling_place_id == "10638":
            record = record._replace(polling_place_easting="442682")
            record = record._replace(polling_place_northing="442998")

        # All Saints Church Church Causeway Thorp Arch Wetherby LS23 7AE
        if record.polling_place_id == "10627":
            record = record._replace(polling_place_easting="443799")
            record = record._replace(polling_place_northing="446079")

        # All Souls Church Blackman Lane Leeds LS2 9EY
        if record.polling_place_id == "10369":
            record = record._replace(polling_place_easting="429940")
            record = record._replace(polling_place_northing="434720")

        # Kentmere Community Centre (Main Hall) Kentmere Avenue Seacroft Leeds LS14 1BW
        if record.polling_place_id == "10289":
            record = record._replace(polling_place_easting="435081")
            record = record._replace(polling_place_northing="436757")

        # Guiseley AFC (Sponsor`s/Director`s Lounges) Nethermoor Park Otley Road Guiseley LS20 8BT
        if record.polling_place_id == "10154":
            record = record._replace(polling_place_easting="418531")
            record = record._replace(polling_place_northing="442305")

        # Haigh Road Community Centre, Haigh Road LS26 0LW
        if record.polling_place_id == "13046":
            record = record._replace(polling_place_easting="434066")
            record = record._replace(polling_place_northing="428893")

        return super().station_record_to_dict(record)
