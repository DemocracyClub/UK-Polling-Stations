from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "WKF"
    addresses_name = "2024-07-04/2024-06-06T14:50:20.339867/Democracy Club - Polling Districts 040724.csv"
    stations_name = "2024-07-04/2024-06-06T14:50:20.339867/Democracy Club - Polling Stations 040724.csv"
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.lstrip("0").strip()

        if uprn in [
            "63205108",  # THE COTTAGE, WENTBRIDGE, PONTEFRACT
            "63111468",  # 14 THE GREEN, SOUTH KIRKBY, PONTEFRACT
            "63194364",  # 2 STARLING WAY, CASTLEFORD
            "63183449",  # 12 OAKDALE DRIVE, SOUTH ELMSALL, PONTEFRACT
            "63183445",  # 37 OAKDALE DRIVE, SOUTH ELMSALL, PONTEFRACT
            "63183151",  # 2 OAKDALE DRIVE, SOUTH ELMSALL, PONTEFRACT
            "63013620",  # EAST FARM BROAD LANE, SOUTH ELMSALL, PONTEFRACT
            "63184405",  # 53 SILCOATES LANE, WRENTHORPE, WAKEFIELD
            "63166997",  # 10 FARGATE CLOSE, SOUTH KIRKBY, PONTEFRACT
            "63185795",  # 46 TURNBERRY AVENUE, ACKWORTH, PONTEFRACT
            "63192244",  # 30 SEALS DRIVE, ACKWORTH, PONTEFRACT
            "63192242",  # 26 SEALS DRIVE, ACKWORTH, PONTEFRACT
            "63192269",  # 104 SEALS DRIVE, ACKWORTH, PONTEFRACT
            "63192275",  # 116 SEALS DRIVE, ACKWORTH, PONTEFRACT
            "63185959",  # PLOT 5 CARAVAN FAIR ACRES WHELDON ROAD, CASTLEFORD
            "63177851",  # FAIR ACRES, WHELDON ROAD, CASTLEFORD
            "63136558",  # WENTBRIDGE HOUSE HOTEL, WENTBRIDGE, PONTEFRACT
            "63059008",  # THE OLD VICARAGE, JACKSONS LANE, WENTBRIDGE, PONTEFRACT
            "63198595",  # CORNER VIEW, HOYLE MILL ROAD, KINSLEY, PONTEFRACT
            "63057162",  # WILLOW TREE FARM, HOYLE MILL ROAD, KINSLEY, PONTEFRACT
            "63155597",  # HOYLE MILL FARM, HOYLE MILL ROAD, KINSLEY, PONTEFRACT
        ]:
            return None

        if record.postcode.strip() in [
            # splits
            "WF11 0FX",
            "WF5 0RT",
            "WF2 0RG",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Station change reuested by council
        # OLD: BRACKENHILL COMMUNITY CENTRE, OFF DICKY SYKES LANE, ACKWORTH, PONTEFRACT, WF7 7AR
        # NEW: ACKWORTH PARISH COUNCIL COMMUNITY CENTRE, BELL LANE, ACKWORTH, WF7 7JH
        if record.stationcode == "010-01NN":
            record = record._replace(
                add1="Bell Lane",
                add2="Ackworth",
                add3="",
                add4="",
                add5="",
                add6="",
                placename="ACKWORTH PARISH COUNCIL COMMUNITY CENTRE",
                postcode="WF7 7JH",
                xordinate="443553",
                yordinate="416345",
            )

        # Remove stations from Leeds and Kirklees
        if record.stationcode in [
            "ODD-132",
            "ODD-133",
            "ODD-134",
            "ODD-135",
            "ODD-136",
            "ODD-137",
            "ODD-138",
            "ODD-139",
            "ODD-140",
            "ODD-141",
            "ODD-142",
            "ODD-143",
            "ODD-144",
            "ODD-145",
            "ODD-146",
            "ODD-147",
            "ODD-148",
            "ODD-149",
            "RL-1",
            "RL-2",
            "RL-3",
            "RL-4",
            "RL-5",
            "RL-6",
            "RL-7",
            "RL-8",
            "RL-9",
        ]:
            return None

        return super().station_record_to_dict(record)
