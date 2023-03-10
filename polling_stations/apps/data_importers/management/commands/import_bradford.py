from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRD"
    addresses_name = (
        "2023-05-04/2023-03-23T11:13:54.869889/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-03-23T11:13:54.869889/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100051130917",  # COTTAGE STANSFIELD ARMS RESTAURANT APPERLEY LANE, APPERLEY BRIDGE, BRADFORD
            "100051942648",  # LOW LODGE, BELGRAVE ROAD, KEIGHLEY
            "10010571811",  # OLD SOUTH BARN, MOOR END, BLACK MOOR ROAD, OXENHOPE, KEIGHLEY
            "10010571812",  # SOUTH BARN COTTAGE, MOOR END, BLACK MOOR ROAD, OXENHOPE, KEIGHLEY
            "10090402080",  # 15 BACK BLYTHE AVENUE, BRADFORD
            "10090402777",  # 37 RED HOLT DRIVE, KEIGHLEY
            "10090978516",  # 7 CHURCH FARM CLOSE, BRADFORD
            "100051268913",  #  382 OAKWORTH ROAD, KEIGHLEY
            "10090404116",  # 382A OAKWORTH ROAD, KEIGHLEY
            "100051268917",  # HILL POINT, OAKWORTH ROAD, KEIGHLEY
            "10091675520",  # 12 BRIGGS WAY, BRADFORD
            "10091675521",  # 10 BRIGGS WAY, BRADFORD
            "10024350071",  # 313A BEACON ROAD, BRADFORD
            "10024070534",  # STEWARDS FLAT HEADLEY GOLF CLUB HEADLEY LANE, THORNTON, BRADFORD
            "10024353033",  # 43 BRONTE CARAVAN PARK HALIFAX ROAD, KEIGHLEY
            "10023347526",  # CATSTONES VIEW, LEES MOOR, KEIGHLEY
            "10002321349",  # STELL HILL BARN, STELL HILL, KEIGHLEY
            "10094182160",  # APARTMENT 2, BANK HOUSE, 49 OTLEY ROAD, SHIPLEY
            "100051288906",  # FLAT 1 BANKDALE HOUSE 69-71 OTLEY ROAD, SHIPLEY
            "100051937333",  # ST. MARY & ST. WALBURGA PRESBYTERY, KIRKGATE, SHIPLEY
            "10093449550",  # 5 RAINES LANE, BINGLEY
            "10023344251",  # FLAT 1, 1 PARK ROAD, BINGLEY
            "10023344253",  # FLAT 3, 1 PARK ROAD, BINGLEY
            "100051226974",  # 2 THORNBURY ROAD, BRADFORD
            "10010579160",  # FLAT AHMADIYYA MUSLIM ASSOCIATION MOSQUE 393 LEEDS ROAD, BRADFORD
            "100051186198",  # 926B LEEDS ROAD, BRADFORD
            "10090402562",  # FLAT AT SHOULDER OF MUTTON 28 KIRKGATE, BRADFORD
            "100051167260",  # 896A GREAT HORTON ROAD, BRADFORD
            "100051219010",  # BROGDEN HOUSE FARM 5A SPEN VIEW LANE, BRADFORD
            "10023347525",  # CRAGG VIEW FARM, LEES MOOR, KEIGHLEY
            "10023347524",  # CRAGG VIEW BARN, LEES MOOR, KEIGHLEY
        ]:
            return None

        if record.addressline6 in [
            # splits
            "BD1 2PJ",
            "LS29 6QJ",
            "BD22 0ER",
            "BD15 7WB",
            "BD10 8LL",
            "BD8 9NW",
            "BD9 6AS",
            "BD16 1NT",
            "BD7 4RA",
            "BD12 8EW",  # WYKE, BRADFORD
            "BD12 8EY",  # WYKE, BRADFORD
            "BD13 3SD",  # 1-4 THORNGATE, THORNTON, BRADFORD
            "BD22 9RQ",  # HAWORTH, KEIGHLEY
            "BD17 5DH",  # BAILDON, SHIPLEY
            "BD3 9TY",  # FLAT 1-4 818 LEEDS ROAD, BRADFORD
            "BD1 4AB",  # 20-22 MILL STREET, BRADFORD
        ]:
            return None

        return super().address_record_to_dict(record)
