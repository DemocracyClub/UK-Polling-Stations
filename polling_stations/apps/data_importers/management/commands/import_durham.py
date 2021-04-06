from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DUR"
    addresses_name = "2021-03-19T15:47:40.490727/durham_deduped.csv"
    stations_name = "2021-03-19T15:47:40.490727/durham_deduped.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200002975735",  # 2 HIGH BRADLEY, WOLSINGHAM, BISHOP AUCKLAND
            "200002975734",  # 1 HIGH BRADLEY, WOLSINGHAM, BISHOP AUCKLAND
            "10070414854",  # HIGH STONECHESTER FARM, HAMSTERLEY, BISHOP AUCKLAND
            "100110519859",  # 2 REGENT STREET, ELDON LANE, BISHOP AUCKLAND
            "10091173970",  # BARNSIDE COTTAGE, BOWES ROAD, BARNARD CASTLE
            "10014554487",  # 65A COCKTON HILL ROAD, BISHOP AUCKLAND
            "100110483833",  # 58 SHAFTO WAY, NEWTON AYCLIFFE
            "100110483832",  # 56 SHAFTO WAY, NEWTON AYCLIFFE
            "100110483831",  # 54 SHAFTO WAY, NEWTON AYCLIFFE
            "100110483830",  # 52 SHAFTO WAY, NEWTON AYCLIFFE
            "100110483829",  # 50 SHAFTO WAY, NEWTON AYCLIFFE
            "100110748946",  # 53A CHEAPSIDE, SPENNYMOOR
            "10093427172",  # THE STABLES, BENT HOUSE LANE, DURHAM
            "10001010514",  # BLUE BARN, OLD CASSOP, DURHAM
            "10001010513",  # STRAWBERRY HILL BARN, OLD CASSOP, DURHAM
            "10001010515",  # SWALLOW RIDGE BARN, OLD CASSOP, DURHAM
            "10014561118",  # OAK TREE BARN, SALTERS LANE, TRIMDON, TRIMDON STATION
            "10093427357",  # 100B SUNDERLAND ROAD, HORDEN
            "10013609644",  # 100 SUNDERLAND ROAD, HORDEN
            "100110772913",  # FLAT CRAGSIDE HOUSE SEASIDE LANE, EASINGTON COLLIERY
            "10013609554",  # GUPTA HOUSE 14 SEASIDE LANE, EASINGTON COLLIERY
            "100110527067",  # 1 FOUNDRY FIELDS, CROOK
            "200002973264",  # FURZEDOWN, LOW JOBS HILL, CROOK
            "100110709958",  # ENDOR, DARLINGTON ROAD, DURHAM
            "10013820903",  # GARDENERS COTTAGE, DARLINGTON ROAD, DURHAM
            "200003214253",  # FAIRFIELD, LOWES BARN BANK, DURHAM
            "100110741529",  # BONA CASA, WOODSIDE, SACRISTON, DURHAM
            "10002955293",  # WILLOW HOUSE, WOODSIDE, SACRISTON, DURHAM
            "200003837208",  # GREENBANK HOUSE, WOODSTONE VILLAGE, HOUGHTON LE SPRING
            "200003837203",  # WILLOW FARM STOVES, WILLOW FARM, WOODSTONE VILLAGE, HOUGHTON LE SPRING
            "100110741309",  # SUMMERHILL, PETH BANK, LANCHESTER, DURHAM
            "200002821450",  # JOHNSON HALL WYNDWAYS DRIVE, DIPTON
            "10014567760",  # FINES HOUSE QUEENS PARADE (SIDE), ANNFIELD PLAIN
            "10094019851",  # OLD FIELD HOUSE, ANNFIELD PLAIN, STANLEY
            "100110707417",  # EAST LODGE, THE HERMITAGE, CHESTER LE STREET
        ]:
            return None

        if record.addressline6 in [
            "SR7 7NE",
            "DL12 9UR",
            "DH1 2RZ",
            "DL4 1DN",
            "SR7 9BS",
            "SR7 7HX",
            "DH8 8HN",
            "DL16 6AJ",
            "DL14 6PP",
            "DL13 1ND",
            "DH2 2BL",
            "DL13 4NQ",
            "DL13 2AB",
            "DL5 5AH",
            "DL16 6XF",
            "DH7 7RD",
            "DL13 5RX",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Forest-of-Teesdale Primary School (2410) Forest in Teesdale Barnard Castle DL12 0HA
        if record.polling_place_id == "52093":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        return super().station_record_to_dict(record)
