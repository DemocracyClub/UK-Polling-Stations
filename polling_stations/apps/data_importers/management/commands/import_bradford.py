from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRD"
    addresses_name = (
        "2024-07-04/2024-06-14T15:57:51.218542/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-14T15:57:51.218542/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
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
                "10024350071",  # 313A BEACON ROAD, BRADFORD
                "10024070534",  # STEWARDS FLAT HEADLEY GOLF CLUB HEADLEY LANE, THORNTON, BRADFORD
                "10024353033",  # 43 BRONTE CARAVAN PARK HALIFAX ROAD, KEIGHLEY
                "10023347526",  # CATSTONES VIEW, LEES MOOR, KEIGHLEY
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
                "10090400394",  # FARMHOUSE GLOVERSHAW FARM GLOVERSHAW LANE, BAILDON
                "10002323379",  # BOTTOM FARM, DOBSON LOCKS, BRADFORD
                "100051198529",  # 66 NEW LANE, BRADFORD
                "100051198526",  # STATION HOUSE, NEW LANE, LAISTERDYKE, BRADFORD
                "100051139467",  # 250 BOWLING BACK LANE, BRADFORD
                "100051950412",  # SCHOOL HOUSE, KNOWLES LANE, BRADFORD
                "10024293191",  # FLAT 1 513 TONG STREET, BRADFORD
                "100051216809",  # 260 SHETCLIFFE LANE, BRADFORD
                "100051216810",  # 262 SHETCLIFFE LANE, BRADFORD
                "100051149485",  # 99 COMMON ROAD, LOW MOOR, BRADFORD
                "200002729422",  # LOWER COLLIER SYKE BARN, SYKE LANE, QUEENSBURY, BRADFORD
                "200002729422",  # LOWER COLLIER SYKE BARN, SYKE LANE, QUEENSBURY, BRADFORD
                "10093447297",  # 1 HUNSBURY CROFT, KEIGHLEY
                "10010586698",  # LOWER HOLME HOUSE, OAKWORTH, KEIGHLEY
                "200001958489",  # 4B ALL SAINTS TERRACE, KEIGHLEY
                "10093451621",  # BAR HOUSE, BAR HOUSE LANE, KEIGHLEY
                "200004698418",  # CROSSMOOR FARM, SKIPTON ROAD, SILSDEN, KEIGHLEY
                "200004710534",  # THE RAIKES RESIDENTIAL HOME, BRADLEY ROAD, SILSDEN, KEIGHLEY
                "100051935972",  # WOODLAND VIEW, PROD LANE, BAILDON, SHIPLEY
                "100051252903",  # BUTTERFLY HALL, LEES MOOR, KEIGHLEY
                "100051934394",  # 88 OAKS LANE, ALLERTON, BRADFORD
                "10023348536",  # FLAT AT 1 SILKSTONE ROAD, BRADFORD
                "100051143760",  # 2 BURNSALL ROAD, BRADFORD
                "100051143759",  # 1 BURNSALL ROAD, BRADFORD
                "100051152153",  # 2 CURZON ROAD, BRADFORD
                "10002322546",  # FLAT 13, BYRON HALLS, BYRON STREET, BRADFORD
                "10090675725",  # SOUTH STREET NEWS AND WINE, FLAT AT 84 SOUTH STREET, KEIGHLEY
                "100051270314",  # 90 QUEENS ROAD, KEIGHLEY
                "10090678354",  # HIGH BIRKS FIRE CLAY WORKS BREWERY LANE, THORNTON, BRADFORD
                "10010571446",  # LAUREL BANK, FORD HILL, QUEENSBURY, BRADFORD
                "100051221713",  # 50 STAMFORD STREET, BRADFORD
                "100051951442",  # 302 PARKSIDE ROAD, BRADFORD
                "100051179413",  # FLAT 1 33 HUSTLERGATE, BRADFORD
                "200002415190",  # 14 WILMER ROAD, BRADFORD
                "100051934836",  # ROSE COTTAGE, WAGON LANE, BINGLEY
                "10090404421",  # 2 BIRKSLAND STREET, BRADFORD
                "10010574743",  # SECOND FLOOR 11 UPPER MILLERGATE, BRADFORD
                "10090402475",  # FLAT 514 THORNTON ROAD, BRADFORD
                "100051137696",  # 26 BIRCH STREET, BRADFORD
                "100051137695",  # 25 BIRCH STREET, BRADFORD
                "10010587879",  # 3A DUCKWORTH LANE, BRADFORD
                "10070064587",  # FLAT ABOVE THE HOCKNEY 3 DALE STREET, SHIPLEY
                "100051164196",  # 213A GAIN LANE, FAGLEY, BRADFORD
                "100051168409",  # 12 GREENWOOD DRIVE, BRADFORD
                "100051270549",  # HIGHER REDCAR HOUSE, WHITLEY HEAD, STEETON, KEIGHLEY
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "LS29 6QJ",
            "BD15 7WB",
            "BD22 7JU",
            "BD7 4RA",
            "BD1 2PJ",
            "BD6 1HP",
            "BD16 1NT",
            "BD10 8FB",
            "BD10 8LL",
            "BD22 0ER",
            "BD8 9NW",
            # suspect
            "BD12 8EW",
            "BD12 8EY",
            "BD13 3SD",
            "BD22 9RQ",
            "BD17 5DH",
            "BD3 9TY",
            "BD3 8EZ",
            "BD1 4AB",
            "BD4 0RJ",
            "BD12 0AQ",
            "BD15 7UE",
            "BD15 7AB",
            "BD15 7SQ",
            "BD21 1AX",
            "BD13 2JR",
            "BD4 7PG",
            "BD5 7DP",
            "BD4 7TL",
            "BD12 9EU",
            "BD8 9NY",
        ]:
            return None

        return super().address_record_to_dict(record)
