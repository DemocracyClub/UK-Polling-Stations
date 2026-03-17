from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LDS"
    addresses_name = "2026-05-07/2026-03-23T13:53:24.869634/Democracy_Club__07May2026 amended version.tsv"
    stations_name = "2026-05-07/2026-03-23T13:53:24.869634/Democracy_Club__07May2026 amended version.tsv"
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # removing bad coordinates for:
        # Central Methodist Church, (Church Hall) (Desk B), 10a Wesley Street, Morley, Leeds
        # Central Methodist Church, (Church Hall) (Desk A), 10a Wesley Street, Morley, Leeds
        if record.polling_place_id in [
            "26864",
            "26662",
        ]:
            record = record._replace(
                polling_place_easting="0",
                polling_place_northing="0",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "72132919",  # EBOR COTTAGE, MIDDLETON ROAD, LEEDS
            "72721195",  # FLAT PENDAS ARMS NABURN APPROACH, WHINMOOR, LEEDS
            "72665355",  # THE BEECHES, WIGHILL, TADCASTER
            "72390208",  # THE GABLES, BARROWBY LANE, GARFORTH, LEEDS
            "72652486",  # FIRS HILL FARM, POOL BANK NEW ROAD, POOL IN WHARFEDALE, OTLEY
            "72528574",  # BANKEND FARM, BEDLAM LANE, ARTHINGTON, OTLEY
            "72536279",  # THE LODGE, LOW LANE, HORSFORTH, LEEDS
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
            "72658394",  # ELLIS HOUSE, BRIDGE HOUSE, GLEDHOW LANE, LEEDS
        ]:
            return None

        if record.addressline6 in [
            # SPLIT
            "LS10 4AZ",
            "LS10 4BD",
            "LS12 2BN",
            "LS13 3DX",
            "LS14 1QA",
            "LS14 1QX",
            "LS15 8JZ",
            "LS16 7SU",
            "LS17 9ED",
            "LS25 1AX",
            "LS8 1NG",
            "LS8 2QG",
            "LS9 6LP",
            "WF3 1GQ",
            "WF3 1TB",
            # WRONG
            "LS2 7DJ",
            "LS9 8DU",
            "LS15 8FD",
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
