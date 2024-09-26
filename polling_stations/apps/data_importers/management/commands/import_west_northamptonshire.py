from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WNT"
    addresses_name = (
        "2024-07-04/2024-05-30T19:31:15.536348/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-05-30T19:31:15.536348/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "28017243",  # WOODYARD COTTAGE, WATLING STREET, WEEDON, NORTHAMPTON
                "28042085",  # 1 BYFIELD ROAD, WOODFORD HALSE, DAVENTRY
                "28048536",  # NEW LEAF FARM, CHURCH STREET, BYFIELD, DAVENTRY
                "10093938068",  # MOBILE HOME OAKWOOD BARN LEICESTER LANE, EYDON
                "10093936580",  # OAKWOOD BARN, LEICESTER LANE, EYDON, DAVENTRY
                "10093937623",  # THE STUDIO, PURSTON ROAD, PURSTON, BRACKLEY
                "10093935887",  # THE FOLLY, PURSTON ROAD, PURSTON, BRACKLEY
                "10093937913",  # 60 HIGH STREET, BRACKLEY
                "100032141487",  # FLAT GROUND FLOOR 88 HIGH STREET, BRACKLEY
                "100032141485",  # FLAT FIRST FLOOR 84 HIGH STREET, BRACKLEY
                "100032141484",  # FLAT GROUND FLOOR 82 HIGH STREET, BRACKLEY
                "10093937561",  # 2 BUCKINGHAM ROAD, SILVERSTONE
                "10023964175",  # THE GRANGE HOUSE HAYES FARM ABTHORPE ROAD, SILVERSTONE
                "10013091463",  # HAYES FARMHOUSE HAYES FARM ABTHORPE ROAD, SILVERSTONE
                "200001472626",  # SALCEY CABINET MAKERS LTD, THE HOMESTEAD, WATLING STREET, POTTERSPURY, TOWCESTER
                "10023963859",  # HOMESTEAD FARM, WATLING STREET, POTTERSPURY, TOWCESTER
                "10023963859",  # HOMESTEAD FARM, WATLING STREET, POTTERSPURY, TOWCESTER
                "10095797189",  # 68 AINTREE AVENUE, TOWCESTER
                "10095794655",  # 29 EARLS FARM WAY, TOWCESTER
                "10000463708",  # PAYNES NURSERIES LTD, 192 WATLING STREET EAST, TOWCESTER
                "10091706476",  # THE FLAT 201 WATLING STREET WEST, TOWCESTER
                "10095800148",  # APPLE TREE LODGE, BLAKESLEY ROAD, MAIDFORD, TOWCESTER
                "15076305",  # OLD LODGE, LONDON ROAD, COLLINGTREE, NORTHAMPTON
                "10000461084",  # HOUGHTON GAME FARM, LEYS LANE, GREAT HOUGHTON, NORTHAMPTON
                "10013088990",  # FLAT THE OLD FORGE WATLING STREET EAST, FOSTERS BOOTH
                "28025465",  # CLAY COTTAGE, HOLLOWELL ROAD, CREATON, NORTHAMPTON
                "15108843",  # 5 MANDERVILLE CLOSE, NORTHAMPTON
                "15108659",  # 121 ADNITT ROAD, NORTHAMPTON
                "15108660",  # 123 ADNITT ROAD, NORTHAMPTON
                "15037200",  # 23 MAGEE STREET, NORTHAMPTON
                "15113696",  # 19 REGENT SQUARE, NORTHAMPTON
                "15129122",  # 73A SPENCER BRIDGE ROAD, NORTHAMPTON
                "15061130",  # THE WHEATSHEAF, 126 DALLINGTON ROAD, NORTHAMPTON
                "15055929",  # 4 WESTERN VIEW, NORTHAMPTON
                "10023965609",  # TOP FARM HOUSE TOP FARM NORTHAMPTON ROAD, TIFFIELD
                "200001477054",  # FLITTON HILLS FARM HOUSE FLITTON HILLS FARM EASTCOTE ROAD, TIFFIELD
                "15043715",  # 99 BOUGHTON GREEN ROAD, NORTHAMPTON
                "15054454",  # 105 ST. ANDREWS ROAD, NORTHAMPTON
                "15126528",  # 103B ST. ANDREWS ROAD, NORTHAMPTON
                "15089445",  # 103A ST, ANDREWS ROAD, NORTHAMPTON
                "10013088753",  # FLAT VERSION FARM TURWESTON ROAD, TURWESTON
                "28047695",  # WESTCOMBE FARM, FAWSLEY, DAVENTRY
                "28021613",  # SYBOLE FARM, SOUTH KILWORTH ROAD, WELFORD, NORTHAMPTON
                "28032688",  # STARRS LODGE, CLIPSTON ROAD, MARSTON TRUSSELL, MARKET HARBOROUGH
                "200001816977",  # PEAS FURLONG COTTAGE, CULWORTH, BANBURY
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "NN2 7EL",
            "NN6 9HG",
            "NN11 6YH",
            # looks wrong
            "NN13 7DP",
            "NN3 6QU",
            "NN3 8NU",
            "NN2 7JP",
            "NN1 2FE",
            "NN5 7EE",
            "NN3 3EW",
            "NN7 4LB",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # adding postcode for: Farthinghoe Village Hall, Cockley Road, Farthinghoe, Brackley, NN13 6UF
        if record.polling_place_id == "42886":
            record = record._replace(polling_place_postcode="NN13 5PD")

        # adding postcode for: Stoke Bruerne Village Hall, Church Lane, Stoke Bruerne, Towcester
        if record.polling_place_id == "43019":
            record = record._replace(polling_place_postcode="NN12 7SG")

        # point correction for: Mobile Unit, Local Centre Car Park, Bordeaux Close, Off Weggs Farm Road, Alsace Park, Northampton, NN5 6YR
        if record.polling_place_id == "42721":
            record = record._replace(polling_place_easting="470877")
            record = record._replace(polling_place_northing="262278")

        # adding postcode for: Brackley Recreation Centre, Sports Hall, Springfield Way, Brackley
        if record.polling_place_id == "43074":
            record = record._replace(polling_place_postcode="NN13 6JJ")

        return super().station_record_to_dict(record)
