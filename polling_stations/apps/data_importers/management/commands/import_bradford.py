from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRD"
    addresses_name = "2021-03-10T21:40:19.803040/Bradford Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-10T21:40:19.803040/Bradford Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Toller Youth Cafe, 2 Duckworth Lane, Bradford
        if record.polling_place_id == "25993":
            record = record._replace(polling_place_easting="414102")
            record = record._replace(polling_place_northing="434471")

        # St John`s Church South Street Keighley BD22 7BU
        if record.polling_place_id == "26270":
            record = record._replace(polling_place_easting="405613")
            record = record._replace(polling_place_northing="439897")

        # Classroom At Lodge Cafe Bowling Park Lodge Bowling Hall Road Bradford
        if record.polling_place_id == "26240":
            record = record._replace(polling_place_easting="417437")
            record = record._replace(polling_place_northing="431215")

        # Station change - https://trello.com/c/mzcaj34E/346-bradford
        if record.polling_place_id == "26043":
            record = record._replace(
                polling_place_name="Wibsey Methodist Church",
                polling_place_address_1="School Lane",
                polling_place_address_2="Bradford",
                polling_place_address_3="",
                polling_place_easting="414973",
                polling_place_northing="430159",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100051942648",  # STEWARDS FLAT HEADLEY GOLF CLUB HEADLEY LANE, THORNTON, BRADFORD
            "10090402777",  # OLD SOUTH BARN, MOOR END, BLACK MOOR ROAD, OXENHOPE, KEIGHLEY
            "100051268913",  # SOUTH BARN COTTAGE, MOOR END, BLACK MOOR ROAD, OXENHOPE, KEIGHLEY
            "100051268917",  # STELL HILL BARN, STELL HILL, KEIGHLEY
            "10002321349",  # CLARK HOUSE COTTAGE, WEST LANE, BAILDON, SHIPLEY
            "10024353033",  # 382 OAKWORTH ROAD, KEIGHLEY
            "10010571811",  # HILL POINT, OAKWORTH ROAD, KEIGHLEY
            "10010571812",  # LOW LODGE, BELGRAVE ROAD, KEIGHLEY
            "100051293123",  # 7 CHURCH FARM CLOSE, BRADFORD
            "100051293145",  # 72 WEST LANE, BAILDON, SHIPLEY
            "10024070655",  # ASHLEA, WEST LANE, BAILDON, SHIPLEY
            "100051293144",  # 4 BARNSTAPLE WAY, BRADFORD
            "100051293142",  # 6 BARNSTAPLE WAY, BRADFORD
            "100051122920",  # CLARKE HOUSE FARM, WEST LANE, BAILDON, SHIPLEY
            "10024070534",  # COTTAGE STANSFIELD ARMS RESTAURANT APPERLEY LANE, APPERLEY BRIDGE, BRADFORD
            "10090402080",  # SCHOOL HOUSE, WEST LANE, BAILDON, SHIPLEY
            "10023348334",  # HIGH BIRKS FIRE CLAY WORKS BREWERY LANE, THORNTON, BRADFORD
            "10090402562",  # 15 BACK BLYTHE AVENUE, BRADFORD
            "10094870940",  # FLAT AT THE BLACK SWAN 150 THORNTON ROAD, BRADFORD
            "10090678354",  # 10 BRIGGS WAY, BRADFORD
            "10023347357",  # 12 BRIGGS WAY, BRADFORD
            "200001104554",  # HIGHLANDS, LEE LANE, BINGLEY
            "200001104555",  # FLAT AT THE NEWBY SQUARE BOWLING OLD LANE, BRADFORD
            "10090978516",  # 926B LEEDS ROAD, BRADFORD
            "100051186198",  # 43 BRONTE CARAVAN PARK HALIFAX ROAD, KEIGHLEY
            "100051226974",  # FLAT AT SHOULDER OF MUTTON 28 KIRKGATE, BRADFORD
            "100051130917",  # 2 THORNBURY ROAD, BRADFORD
            "10091675521",  # 37 RED HOLT DRIVE, KEIGHLEY
            "10091675520",  # FLAT AT THE DRUM WINDER THORPE CHAMBERS 12A IVEGATE, BRADFORD
            "10023347524",  # CRAGG VIEW BARN, LEES MOOR, KEIGHLEY
            "10023347525",  # CRAGG VIEW FARM, LEES MOOR, KEIGHLEY
        ]:
            return None

        if record.addressline6 in [
            "BD13 3SD",
            "BD1 3PP",
            "BD1 4AB",
            "BD1 1NE",
            "BD1 1SX",
            "BD1 1SR",
            "BD1 1JB",
            "BD5 7DP",
            "BD4 9AN",
            "BD3 9TY",
            "BD16 1NT",
            "BD15 7WB",
            "BD7 4RA",
            "LS29 6QJ",
            "BD6 2NQ",
            "BD9 6AS",
        ]:
            return None

        return super().address_record_to_dict(record)
