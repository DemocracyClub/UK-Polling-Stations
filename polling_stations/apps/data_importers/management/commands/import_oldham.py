from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "OLD"
    addresses_name = (
        "2022-05-05/2022-02-22T14:42:39.316671/Democracy_Club__05May2022 (2).tsv"
    )
    stations_name = (
        "2022-05-05/2022-02-22T14:42:39.316671/Democracy_Club__05May2022 (2).tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Coldhurst Lifelong Learning Centre Rochdale Road Oldham OL1 2JD
        if record.polling_place_id == "8903":
            record = record._replace(polling_place_postcode="OL1 2HR")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100011199050",  # 109 BROADWAY, ROYTON, OLDHAM
            "100011199092",  # 144 BROADWAY, ROYTON, OLDHAM
            "100011210768",  # 83 DERBY STREET, OLDHAM
            "422000014564",  # 81 DERBY STREET, CHADDERTON, OLDHAM
            "422000014571",  # 91 DERBY STREET, CHADDERTON, OLDHAM
            "422000034427",  # 66 ROMAN ROAD, FAILSWORTH, MANCHESTER
            "422000036274",  # 2 SCHOLES STREET, FAILSWORTH, MANCHESTER
            "422000046320",  # 40 TANDLEWOOD PARK, ROYTON, OLDHAM
            "422000060807",  # DOLEFIELD BARN, FUR LANE, GREENFIELD, OLDHAM
            "422000061537",  # 81 OLDHAM ROAD, GRASSCROFT, OLDHAM
            "422000064639",  # 2 STONEBOTTOM BROW, DOBCROSS, OLDHAM
            "422000064640",  # 4 STONEBOTTOM BROW, DOBCROSS, OLDHAM
            "422000065012",  # LOWER SLACK, SLACKGATE LANE, DENSHAW, OLDHAM
            "422000066942",  # 2 COOPER STREET, SPRINGHEAD, OLDHAM
            "422000069004",  # 3 STATION LANE, GREENFIELD, OLDHAM
            "422000098508",  # WHITFIELD COTTAGE, WHITFIELD, SHAW, OLDHAM
            "422000102588",  # FLAT 2 76-78 MILNROW ROAD, SHAW
            "422000102589",  # FLAT 1 76-78 MILNROW ROAD, SHAW
            "422000107838",  # 16 CORBETT WAY, DENSHAW, OLDHAM
            "422000112010",  # TURNING POINT BIRCHWOOD, BIRCHWOOD NURSING HOME, LEES NEW ROAD, OLDHAM
            "422000112170",  # MANOR HOUSE FARM, STANDEDGE, DELPH, OLDHAM
            "422000112176",  # BENTLEY FARM, STANDEDGE, DELPH, OLDHAM
            "422000112177",  # STANDEDGE FOOT FARM, STANDEDGE, DELPH, OLDHAM
            "422000113798",  # 1 NEAR SPRINGS, STANDEDGE, DELPH, OLDHAM
            "422000119217",  # 1 FITTON STREET, ROYTON, OLDHAM
            "422000119510",  # FALCONERS ARMS HOLLINS ROAD, OLDHAM
            "422000120352",  # FLAT 1 THE BUNGALOW 43 GRAINS ROAD, DELPH
            "422000120353",  # FLAT 2 THE BUNGALOW 43 GRAINS ROAD, DELPH
            "422000120354",  # FLAT 3 THE BUNGALOW 43 GRAINS ROAD, DELPH
            "422000120355",  # FLAT 4 THE BUNGALOW 43 GRAINS ROAD, DELPH
            "422000120408",  # VALE COTTAGE, STANDEDGE, DELPH, OLDHAM
            "422000124671",  # 239 OLDHAM ROAD, SPRINGHEAD, OLDHAM
            "422000125257",  # 80 EUSTACE STREET, CHADDERTON, OLDHAM
            "422000125258",  # 82 EUSTACE STREET, CHADDERTON, OLDHAM
            "422000126990",  # 556B CHAMBER ROAD, OLDHAM
            "422000129006",  # 189B OLDHAM ROAD, SPRINGHEAD, OLDHAM
            "422000129256",  # 14 MANCHESTER ROAD, GREENFIELD, OLDHAM
            "422000129521",  # 237 COALSHAW GREEN ROAD, CHADDERTON, OLDHAM
            "422000130564",  # INTAKE FARM STANDEDGE HUDDERSFIELD ROAD, DELPH
        ]:
            return None

        if record.addressline6 in [
            "M35 9JU",
            "OL2 8DF",
            "OL2 8DT",
            "OL2 8TN",
            "OL8 1DD",
            "OL8 1HF",
            "OL8 2NE",
            "OL8 3SF",
            "OL9 6BB",
        ]:
            return None

        return super().address_record_to_dict(record)
