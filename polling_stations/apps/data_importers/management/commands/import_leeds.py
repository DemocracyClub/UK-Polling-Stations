from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LDS"
    addresses_name = "2024-05-02/2024-03-19T14:32:27.465948/leeds_deduplicated.tsv"
    stations_name = "2024-05-02/2024-03-19T14:32:27.465948/leeds_deduplicated.tsv"
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "72132919",  # EBOR COTTAGE, MIDDLETON ROAD, LEEDS
            "72721195",  # FLAT PENDAS ARMS NABURN APPROACH, WHINMOOR, LEEDS
            "72665355",  # THE BEECHES, WIGHILL, TADCASTER
            "72390208",  # THE GABLES, BARROWBY LANE, GARFORTH, LEEDS
            "72652486",  # FIRS HILL FARM, POOL BANK NEW ROAD, POOL IN WHARFEDALE, OTLEY
            "72528574",  # BANKEND FARM, BEDLAM LANE, ARTHINGTON, OTLEY
            "72305010",  # THE BUNGALOW, DRURY LANE, HORSFORTH, LEEDS
            "72304132",  # 34 ALEXANDRA ROAD, HORSFORTH, LEEDS
            "72304134",  # 36 ALEXANDRA ROAD, HORSFORTH, LEEDS
            "72304135",  # 37 ALEXANDRA ROAD, HORSFORTH, LEEDS
            "72304136",  # 38 ALEXANDRA ROAD, HORSFORTH, LEEDS
            "72304137",  # 39 ALEXANDRA ROAD, HORSFORTH, LEEDS
            "72304138",  # 40 ALEXANDRA ROAD, HORSFORTH, LEEDS
            "72304139",  # 41 ALEXANDRA ROAD, HORSFORTH, LEEDS
            "72304140",  # 42 ALEXANDRA ROAD, HORSFORTH, LEEDS
            "72304141",  # 43 ALEXANDRA ROAD, HORSFORTH, LEEDS
            "72304142",  # 44 ALEXANDRA ROAD, HORSFORTH, LEEDS
            "72304143",  # 45 ALEXANDRA ROAD, HORSFORTH, LEEDS
            "72304144",  # 46 ALEXANDRA ROAD, HORSFORTH, LEEDS
            "72304145",  # 47 ALEXANDRA ROAD, HORSFORTH, LEEDS
            "72304147",  # 49 ALEXANDRA ROAD, HORSFORTH, LEEDS
            "72536279",  # THE LODGE, LOW LANE, HORSFORTH, LEEDS
            "72108807",  # 145 KENTMERE AVENUE, LEEDS
            "72719195",  # FLAT THE SPORTSMAN STONEY ROCK LANE, BURMANTOFTS, LEEDS
            "72700401",  # FLAT THE REGENT 109 KIRKGATE, LEEDS
            "72721594",  # FLAT THE DUCK AND DRAKE INN 43 KIRKGATE, LEEDS
            "72160712",  # 29 PRESTON PARADE, LEEDS
            "72160713",  # 30 PRESTON PARADE, LEEDS
            "72160714",  # 31 PRESTON PARADE, LEEDS
            "72160715",  # 32 PRESTON PARADE, LEEDS
            "72201722",  # 22 STRATFORD TERRACE, LEEDS
            "72663962",  # 26A STRATFORD TERRACE, LEEDS
            "72659064",  # ROOM 2 22 STRATFORD TERRACE, LEEDS
            "72686179",  # FLAT STAR INN 205 TONG ROAD, FARNLEY, LEEDS
            "72288076",  # 58 INTAKE ROAD, PUDSEY
            "72288078",  # 60 INTAKE ROAD, PUDSEY
            "72288079",  # 62 INTAKE ROAD, PUDSEY
            "72288080",  # 64 INTAKE ROAD, PUDSEY
            "72288081",  # 66 INTAKE ROAD, PUDSEY
        ]:
            return None

        if record.addressline6 in [
            # SPLIT
            "LS10 4BD",
            "LS7 2HN",
            "WF3 2GN",
            "LS10 4AZ",
            "LS12 2BN",
            "LS25 1AX",
            "WF3 1TB",
            "LS9 6LP",
            "LS15 8JZ",
            "LS13 3DX",
            "WF3 2GL",
            "LS15 0LG",
            "WF3 1GQ",
            "LS17 9ED",
            "LS16 7SU",
            "WF3 1FX",
            "LS18 5HN",
            "LS8 2QG",
            # WRONG
            "LS2 7DJ",
            "LS9 8DU",
            "LS22 6RF",
            "LS15 8FD",
            "LS15 8QP",
            "LS18 5EU",
            "LS16 6FE",
            "LS15 8TZ",
            "LS15 8RQ",
            "LS15 8RG",
            "WF3 3LS",
            "LS11 7PQ",
        ]:
            return None

        return super().address_record_to_dict(record)
