from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "AMB"
    addresses_name = "2024-07-04/2024-06-14T12:39:27.733042/AMB_PD_combined.csv"
    stations_name = "2024-07-04/2024-06-14T12:39:27.733042/AMB_PS_combined.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if uprn in [
            "10013426910",  # 21 DALBY GREEN CLOSE, WAINGROVES, RIPLEY
            "10013426909",  # 22 DALBY GREEN CLOSE, WAINGROVES, RIPLEY
            "100030026160",  # 2 BROADWAY, HEANOR
            "100030030700",  # 44 OLD COPPICE SIDE, HEANOR
            "10013423826",  # 2 WIRKSWORTH ROAD, DUFFIELD, BELPER
            "100030024687",  # 10 WIRKSWORTH ROAD, DUFFIELD, BELPER
            "100030024683",  # 6A WIRKSWORTH ROAD, DUFFIELD, BELPER
            "100030024685",  # 8 WIRKSWORTH ROAD, DUFFIELD, BELPER
            "10000254674",  # BLACK BARN, WIRKSWORTH ROAD, DUFFIELD, BELPER
            "200000393745",  # CUMBERHILL LODGE, QUARNDON, DERBY
            "100030010872",  # AMBERDALE, ASHBOURNE ROAD, TURNDITCH, BELPER
            "200000390909",  # POSTERN HOUSE, TURNDITCH, BELPER
            "200000392363",  # SOUTHVIEW, OLD HILLCLIFF LANE, HILLCLIFF LANE, TURNDITCH, BELPER
            "100030011186",  # 50 BAKERS HILL, HEAGE, BELPER
            "10094136152",  # 2 TAYLOR WAY, SWANWICK, ALFRETON
            "100030005756",  # HAYER OFF LICENCE, 101 MANSFIELD ROAD, ALFRETON
            "10000189348",  # VALLEY VIEW, WINDLEY, BELPER
            "10000189632",  # THE SUNDIAL, WINDLEY, BELPER
            "10000189294",  # GREENHILLS, WINDLEY, BELPER
            "200000385731",  # THE SMITHY, KEDLESTON, QUARNDON, DERBY
            "200000391509",  # SYCAMORE FARM, PLAISTOW GREEN, MATLOCK
            "100030025323",  # P E YATES, CHAMPION FARM, QUARNDON, DERBY
            "200000393166",  # BLACK FIRS FARM, ALDERWASLEY, BELPER
            "200000390930",  # PALEROW FARM, SHOTTLE, BELPER
        ]:
            return None

        if record.postcode in [
            # looks wrong
            "DE5 3DJ",
            "DE5 3LA",
            "DE56 2DP",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Removes wrong point for: SOMERCOTES PARISH HALL Nottingham Road Somercotes Alfreton Derbyshire DE55 4LY
        if record.stationcode in [
            "AV93",
            "AV94",
        ]:
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)
