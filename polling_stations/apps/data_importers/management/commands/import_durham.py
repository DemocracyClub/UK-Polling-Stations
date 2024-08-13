from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DUR"
    addresses_name = (
        "2024-07-04/2024-05-29T22:01:24.371874/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-29T22:01:24.371874/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "200002975735",  # 2 HIGH BRADLEY, WOLSINGHAM, BISHOP AUCKLAND
                "200002975734",  # 1 HIGH BRADLEY, WOLSINGHAM, BISHOP AUCKLAND
                "10070414854",  # HIGH STONECHESTER FARM, HAMSTERLEY, BISHOP AUCKLAND
                "10091173970",  # BARNSIDE COTTAGE, BOWES ROAD, BARNARD CASTLE
                "10093427357",  # 100B SUNDERLAND ROAD, HORDEN
                "10013609644",  # 100 SUNDERLAND ROAD, HORDEN
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
                "10014567760",  # FINES HOUSE QUEENS PARADE (SIDE), ANNFIELD PLAIN
                "10094019851",  # OLD FIELD HOUSE, ANNFIELD PLAIN, STANLEY
                "100110476290",  # 2 AUCKLAND PLACE, NEWTON AYCLIFFE
                "100110712083",  # FLAT WEST VIEW STOCKTON ROAD, SEAHAM
                "10013058536",  # WOODLANDS FARM, SOUTH HETTON, DURHAM
                "100110712020",  # AVELDA, SHOTTON ROAD, HORDEN, PETERLEE
                "100110711512",  # ST, JOSEPHS PRESBYTERY, COAST ROAD, BLACKHALL COLLIERY, HARTLEPOOL
                "10094020519",  # 1A IVATT WALK, SHILDON
                "10012053828",  # THINFORD HOUSE THINFORD LANE, THINFORD
                "10094407025",  # 47 EDISON DRIVE, SPENNYMOOR
                "10012055410",  # CLEARWATER CREEK, DURHAM ROAD, COATHAM MUNDEVILLE, DARLINGTON
                "10094404921",  # THE STABLES, DURHAM ROAD, COATHAM MUNDEVILLE, DARLINGTON
                "10093429956",  # THE HAYLOFT, HILTON, DARLINGTON
                "10014553352",  # CRONKLEY, FOREST IN TEESDALE, BARNARD CASTLE
                "200002973260",  # TREVIAN HOUSE, LOW JOBS HILL, CROOK
                "10001010491",  # BROADGATE FARM, ESH WINNING, DURHAM
                "10000808114",  # PHILLIPPA ROSS & CO, ALLERCLEUGH, WEARHEAD, BISHOP AUCKLAND
                "200002976292",  # ROSE COTTAGE, WESTGATE, BISHOP AUCKLAND
                "100110376637",  # 23A NELSON STREET, CONSETT
                "100110708593",  # THE STABLES BLACKFYNE FARM DURHAM ROAD, BLACKHILL
                "10093043495",  # LUMLEY PARK HOUSE COTTAGE FORGE LANE, CASTLE DENE
                "10013259154",  # FLAT AT PROSPECT BUILDINGS COAST ROAD, HORDEN
                "200003644244",  # 7 HOLBORN STREET, SPENNYMOOR
                "200003645831",  # 39 KEMBLE GREEN EAST, NEWTON AYCLIFFE
                "10014556760",  # LONGFIELD BARNARD CASTLE SCHOOL NEWGATE, BARNARD CASTLE
                "10093043991",  # 1 FRONT STREET FLEMING FIELD TRACK TO NORTH MOOR FARM, HASWELL
                "200003218251",  # 1 THE GATEHOUSE KEPIER FARM KEPIER LANE, GILESGATE
                "100110710484",  # ANNFIELD HOUSE, NEWHOUSE ROAD, ESH WINNING, DURHAM
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "DH7 6FR",
            "SR7 9BS",
            "DH9 9JQ",
            "DL13 4NQ",
            "DL12 8JF",
            "DL13 2AB",
            "DH8 8HN",
            "DL16 6AJ",
            "DH2 2BL",
            "DL12 9UR",
            "DL4 1DN",
            "SR7 7NE",
            "DL13 1ND",
            # looks wrong
            "DL5 5QS",
            "DH9 6SA",
            "DH2 2FL",
            "DH7 6NY",
            "DH7 7RD",
            "DH1 4DX",
            "DL5 5AH",
            "DL16 6XF",
        ]:
            return None

        return super().address_record_to_dict(record)
