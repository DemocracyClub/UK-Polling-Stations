from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SHF"
    addresses_name = "2024-07-04/2024-06-03T10:21:10.582196/Eros_SQL_Output001.csv"
    stations_name = "2024-07-04/2024-06-03T10:21:10.582196/Eros_SQL_Output001.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "100052101093",  # BROOKFIELD, LONG LANE, STANNINGTON, SHEFFIELD
                "100051016653",  # EDENFIELD, LONG LANE, STANNINGTON, SHEFFIELD
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
                "100051088863",  # KNOWLE HILL, STREETFIELDS, HALFWAY, SHEFFIELD
                "10003573833",  # GROUNDS PLUS, UNIT 6 LONG ACRE WAY, SHEFFIELD
                "10023151677",  # 8A SOUTHEY GREEN ROAD, SHEFFIELD
                "100050944918",  # 1 COLLINGBOURNE DRIVE, SOTHALL, SHEFFIELD
                "100051021259",  # MOOR HOUSE FARM, STOCKSBRIDGE, SHEFFIELD
                "10013554418",  # WIND HILL FARM, STOCKSBRIDGE, SHEFFIELD
                "100051111037",  # 647 WHITLEY LANE, GRENOSIDE, SHEFFIELD
                "100051111039",  # SYCAMORE FARM, WHITLEY LANE, GRENOSIDE, SHEFFIELD
                "10091127976",  # OLD CROWN INN, MANAGERS ACCOMMODATION 710 PENISTONE ROAD, OWLERTON, SHEFFIELD
                "10013159771",  # CRAWSHAW FARM, UGHILL, BRADFIELD, SHEFFIELD
                "10091733736",  # 386A STANNINGTON ROAD, SHEFFIELD
                "10093467393",  # 5 WOOD STREET, SHEFFIELD
                "100050912255",  # 800 BARNSLEY ROAD, SHEFFIELD
                "100051016622",  # 101A LONDON ROAD, SHEFFIELD
                "10003574282",  # 79A LONDON ROAD, SHEFFIELD
                "10091129534",  # THE ALBION, MANAGERS ACCOMMODATION 71-75 LONDON ROAD, SHEFFIELD
                "10091129582",  # THE CLUBHOUSE, MANAGERS ACCOMMODATION 13 LONDON ROAD, SHEFFIELD
                "100051058537",  # 55 RAVENCARR ROAD, SHEFFIELD
                "100051058539",  # 59 RAVENCARR ROAD, SHEFFIELD
                "100051058536",  # 53 RAVENCARR ROAD, SHEFFIELD
                "100051058538",  # 57 RAVENCARR ROAD, SHEFFIELD
                "100050920075",  # 101 BIRLEY SPA LANE, SHEFFIELD
                "200003021647",  # WHITE LODGE FARM, HIGH BRADFIELD, BRADFIELD, SHEFFIELD
            ]
        ):
            return None

        if record.housepostcode in [
            # split
            "S1 4TA",
            "S8 0PL",
            "S35 9XS",
            "S10 3LG",
            "S10 3GW",
            # suspect
            "S35 2TQ",
            "S35 2WW",
            "S6 2BH",
            "S6 3ED",
            "S7 1FF",
            "S7 1FH",
            "S2 1BP",
            "S13 7EQ",
        ]:
            return None

        return super().address_record_to_dict(record)
