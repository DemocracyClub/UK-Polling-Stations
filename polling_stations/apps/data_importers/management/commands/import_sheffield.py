from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "SHF"
    addresses_name = "2026-05-07/2026-04-09T10:29:11.580036/Democracy Club - Idox_2026-04-09 10-16.csv"
    stations_name = "2026-05-07/2026-04-09T10:29:11.580036/Democracy Club - Idox_2026-04-09 10-16.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "100051058540",  # 60A RAVENCARR ROAD, SHEFFIELD, S2 1QA
                "100050979318",  # MANAGERS FLAT HARLEY HOTEL 334 GLOSSOP ROAD, SHEFFIELD, S10 2HW
                "100051072752",  # VIEW COTTAGE SHEEPHILL ROAD, SHEFFIELD, S11 7TU
                "10023156883",  # 8B STUMPERLOWE HALL ROAD, SHEFFIELD, S10 3QR
                "100051069483",  # STUBBIN COTTAGE, SANDYGATE LANE, SHEFFIELD, S10 5SQ
                "10091130199",  # 1B LAIRD ROAD, SHEFFIELD, S6 4BS
                "100052094057",  # HALLWOOD HOUSE, PENISTONE ROAD, CHAPELTOWN, SHEFFIELD
                "10013646160",  # THE BUNGALOW, HALLWOOD, PENISTONE ROAD, CHAPELTOWN, SHEFFIELD
                "10022924822",  # 3 WADSLEY LANE, SHEFFIELD
                "100052186977",  # 3 BURTON STREET, SHEFFIELD
                "100052083193",  # WOODCLIFFE HOUSE, WOODCLIFFE, SHEFFIELD
                "100052081136",  # 59 CLARKEHOUSE ROAD, SHEFFIELD
                "100050950378",  # 5 CRUMMOCK ROAD, SHEFFIELD
                "100051115573",  # 5 WOODSEATS ROAD, SHEFFIELD
                "10094515334",  # FLAT, ABOVE 649-651, CHESTERFIELD ROAD, SHEFFIELD
                "10091734040",  # 165B BIRLEY SPA LANE, SHEFFIELD
                "10091734039",  # 165A BIRLEY SPA LANE, SHEFFIELD
                "10003573833",  # GROUNDS PLUS, UNIT 6 LONG ACRE WAY, SHEFFIELD
                "100050944918",  # 1 COLLINGBOURNE DRIVE, SOTHALL, SHEFFIELD
                "100051021259",  # MOOR HOUSE FARM, STOCKSBRIDGE, SHEFFIELD
                "10013554418",  # WIND HILL FARM, STOCKSBRIDGE, SHEFFIELD
                "100051111037",  # 647 WHITLEY LANE, GRENOSIDE, SHEFFIELD
                "10091127976",  # OLD CROWN INN, MANAGERS ACCOMMODATION 710 PENISTONE ROAD, OWLERTON, SHEFFIELD
                "10013159771",  # CRAWSHAW FARM, UGHILL, BRADFIELD, SHEFFIELD
                "100050920075",  # 101 BIRLEY SPA LANE, SHEFFIELD
                "200003021647",  # WHITE LODGE FARM, HIGH BRADFIELD, BRADFIELD, SHEFFIELD
                "100051110508",  # 282 WHITEHOUSE LANE, SHEFFIELD
                "10093467393",  # 5 WOOD STREET, SHEFFIELD
            ]
        ):
            return None

        if record.postcode in [
            # split
            "S2 2SY",
            "S6 4AS",
            "S1 4TA",
            "S35 9XS",
            "S20 4TB",
            "S10 3GW",
            "S6 6AD",
            # suspect
            "S2 1BP",
            "S6 2LN",
            "S17 4DN",
            "S3 7LY",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: Unity Gardens Community Room, 3 Reneville Crescent, Ecclesfield, Sheffield, S35 9DA
        if record.pollingstationnumber == "80":
            record = record._replace(pollingstationpostcode="S5 9DE")
        return super().station_record_to_dict(record)
