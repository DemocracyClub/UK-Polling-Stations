from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNS"
    addresses_name = "2026-05-07/2026-03-24T10:10:33.504953/BNS_districts_UTF8.csv"
    stations_name = "2026-05-07/2026-03-24T10:10:33.504953/BNS_stations.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "2007025965",  # 282 GREEN ROAD, SPRINGVALE, PENISTONE, SHEFFIELD
                "100050648613",  # BIRDWELL LODGE, PILLEY HILL, BIRDWELL, BARNSLEY
                "100050657482",  # 5 SHORT STREET, HOYLAND, BARNSLEY
                "2007028574",  # 20 SHELLEY DRIVE, WOMBWELL, BARNSLEY
                "2007026686",  # 70 PONTEFRACT ROAD, WOMBWELL, BARNSLEY
                "100050627818",  # 2 HAVERLANDS LANE, WORSBROUGH, BARNSLEY
                "100050633651",  # ROSEHILL COTTAGE, ROSEHILL COTTAGES, KERESFORTH ROAD, DODWORTH, BARNSLEY
                "100050654255",  # 61 ROSE HILL DRIVE, DODWORTH, BARNSLEY
                "100050675690",  # HALL GATES, CARR HEAD LANE, BOLTON-UPON-DEARNE, ROTHERHAM
                "2007027407",  # 15 WHINSIDE CRESCENT, THURNSCOE, ROTHERHAM
                "100050682539",  # 39 TUDOR STREET, THURNSCOE, ROTHERHAM
                "100050676574",  # 10 DANE STREET NORTH, THURNSCOE, ROTHERHAM
                "100050682224",  # 46 STUART STREET, THURNSCOE, ROTHERHAM
                "2007028566",  # 43 SHELLEY DRIVE, WOMBWELL, BARNSLEY
                "2007027307",  # 16 SOUTH LEA ROAD, HOYLAND, BARNSLEY
                "100050658780",  # 9 SOUTHGATE, HOYLAND, BARNSLEY
                "100050658781",  # 11 SOUTHGATE, HOYLAND, BARNSLEY
                "100050658782",  # 15 SOUTHGATE, HOYLAND, BARNSLEY
                "100050659590",  # 2 SPRINGWOOD ROAD, HOYLAND, BARNSLEY
                "100050659589",  # 1 SPRINGWOOD ROAD, HOYLAND, BARNSLEY
                "100050622934",  # 60 FEARNLEY ROAD, HOYLAND, BARNSLEY
                "2007023628",  # 1 ROWES COTTAGE HOOD HILL PLANTATION VIEW, HOOD HILL, BARNSLEY
                "10022882692",  # BRUCE LODGE, PILLEY HILLS, TANKERSLEY, BARNSLEY
                "100050670929",  # 2 WILBY LANE, BARNSLEY
                "10032781743",  # 17 GREENFOOT CLOSE, BARNSLEY
                "2007026462",  # 51 FOLLY WAY, BARNSLEY
                "2007026007",  # 67 PRIESTLEY AVENUE, DARTON, BARNSLEY
                "100050613838",  # 3 CHURCHFIELD AVENUE, DARTON, BARNSLEY
                "100050613836",  # 1 CHURCHFIELD AVENUE, DARTON, BARNSLEY
                "100050629142",  # 50 HIGH STREET, ROYSTON, BARNSLEY
                "100050610816",  # WILLOW COTTAGE, CARLTON ROAD, BARNSLEY
                "10032786368",  # HOLLINS WOOD, HERMIT HILL, WORTLEY, SHEFFIELD
            ]
        ):
            return None

        if record.postcode in [
            # splits
            "S72 9EH",
            "S70 6NA",
            # looks wrong
            "S63 0PG",
            "S73 8LA",
            "S74 9AE",
            "S74 9AF",
            "S71 4FU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # more accurate point for: COOPERS SCHOOL OF PERFORMING ARTS, Wade Street, Barnsley, S75 2DY
        if record.stationcode in ["77", "94"]:
            record = record._replace(xordinate="432852", yordinate="406676")

        # more accurate point for: TEMPORARY BUILDING - WOOLLEY COLLIERY, Woolley Colliery Road, Darton, S75 5JF
        if record.stationcode == "37":
            record = record._replace(xordinate="431231", yordinate="410976")

        # more accurate point for: TEMPORARY BUILDING AT GRASMERE CRESCENT, Grasmere Crescent, Staincross, S75 5BE
        if record.stationcode == "33":
            record = record._replace(xordinate="432314", yordinate="410992")

        # more accurate point for: SHAW LANE SPORTS CLUB - Shaw Suite, Shaw Lane, Barnsley, S70 6HZ
        if record.stationcode == "75":
            record = record._replace(xordinate="433482", yordinate="405907")

        return super().station_record_to_dict(record)
