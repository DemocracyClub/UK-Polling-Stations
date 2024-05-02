from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNS"
    addresses_name = (
        "2024-05-02/2024-02-28T14:43:06.389877/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2024-05-02/2024-02-28T14:43:06.389877/Democracy Club - Polling Stations.csv"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "2007025965",  # 282 GREEN ROAD, SPRINGVALE, PENISTONE, SHEFFIELD
            "100050684347",  # WAYSIDE, COPSTER LANE, OXSPRING, SHEFFIELD
            "2007003853",  # 2 COATES GREEN, COPSTER LANE, OXSPRING, SHEFFIELD
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
            "2007025437",  # 57 SCHOOL STREET, THURNSCOE, ROTHERHAM
            "2007025434",  # 51 SCHOOL STREET, THURNSCOE, ROTHERHAM
            "2007027211",  # 64 PITT STREET, WOMBWELL, BARNSLEY
            "2007027207",  # 56 PITT STREET, WOMBWELL, BARNSLEY
            "2007028566",  # 43 SHELLEY DRIVE, WOMBWELL, BARNSLEY
            "2007027307",  # 16 SOUTH LEA ROAD, HOYLAND, BARNSLEY
            "100050658780",  # 9 SOUTHGATE, HOYLAND, BARNSLEY
            "100050658781",  # 11 SOUTHGATE, HOYLAND, BARNSLEY
            "100050658782",  # 15 SOUTHGATE, HOYLAND, BARNSLEY
            "100050637300",  # 1 LONGFIELDS CRESCENT, HOYLAND, BARNSLEY
            "100050659590",  # 2 SPRINGWOOD ROAD, HOYLAND, BARNSLEY
            "100050659589",  # 1 SPRINGWOOD ROAD, HOYLAND, BARNSLEY
            "100050622934",  # 60 FEARNLEY ROAD, HOYLAND, BARNSLEY
            "2007023628",  # 1 ROWES COTTAGE HOOD HILL PLANTATION VIEW, HOOD HILL, BARNSLEY
            "2007017071",  # 34 STONE ROW COURT, TANKERSLEY, BARNSLEY
            "2007017072",  # 36 STONE ROW COURT, TANKERSLEY, BARNSLEY
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
        ]:
            return None

        if record.postcode in [
            # looks wrong
            "S63 0PG",
            "S73 8LA",
            "S74 9AE",
            "S74 9AF",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # bugreport #647
        # remove point for: COOPERS SCHOOL OF PERFORMING ARTS, Wade Street, Barnsley, S75 2DY
        if record.pollingstationid in ["2853", "2854"]:
            record = record._replace(xordinate="", yordinate="")

        # more accurate point for: TEMPORARY BUILDING - WOOLLEY COLLIERY, Woolley Colliery Road, Darton
        if record.pollingstationid == "2828":
            record = record._replace(xordinate="431231")
            record = record._replace(yordinate="410976")

        # more accurate point for: TEMPORARY BUILDING AT GRASMERE CRESCENT, Grasmere Crescent, Staincross
        if record.pollingstationid == "2824":
            record = record._replace(xordinate="432314")
            record = record._replace(yordinate="410992")

        return super().station_record_to_dict(record)
