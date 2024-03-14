from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "WKF"
    addresses_name = "2024-05-02/2024-03-14T09:51:32.250794/20240314 Democracy Club Polling Districts.csv"
    stations_name = "2024-05-02/2024-03-14T09:51:32.250794/20240314 Democracy Club Polling Stations.csv"
    elections = ["2024-05-02"]
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
        # point correction for: THREE LANE ENDS ACADEMY, Methley Road, Castleford, WF10 1PN
        if record.stationcode == "23-03PG":
            record = record._replace(xordinate="441303", yordinate="425532")

        return super().station_record_to_dict(record)
