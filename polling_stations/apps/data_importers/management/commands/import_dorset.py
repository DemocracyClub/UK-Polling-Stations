from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DST"
    addresses_name = (
        "2025-07-24/2025-06-19T14:02:41.428024/Democracy_Club__24July2025_tweaked.csv"
    )
    stations_name = (
        "2025-07-24/2025-06-19T14:02:41.428024/Democracy_Club__24July2025_tweaked.csv"
    )
    elections = ["2025-07-24"]
    csv_delimiter = "\t"

    # Maintaining some exclusions as comments for future reference.

    # def station_record_to_dict(self, record):
    #     # 'Beaminster Public Hall, 8 Fleet Street, Beaminster, DT8 3EF'
    #     if record.polling_place_id == "57550":
    #         record = record._replace(polling_place_uprn="10023243684")

    #     # 'Colehill Village Hall - Station 1, 2, 3, Cannon Hill Road, Colehill, Wimborne, BH21 2LS'
    #     if record.polling_place_id in ["58337", "58341", "58389"]:
    #         record = record._replace(polling_place_postcode="BH21 2LR")

    #     # 'Sherborne Scout Hall, Blackberry Lane, Sherborne, DT9 4DE'
    #     if record.polling_place_id == "57906":
    #         record = record._replace(
    #             polling_place_uprn="100041123477"
    #         )  # from addressbase

    #     # 'Scott Estate Office, South Street, Kingston, BH20 5LL' (id: 57470)
    #     if record.polling_place_id == "57470":
    #         record = record._replace(polling_place_postcode="")  # addressbase: BH20 5LQ

    #     return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6.strip() in [
            # split
            "BH19 2PG",
            # suspect
            # "BH19 1DQ",
            # "BH19 1BS",
            # "BH19 1LD",
            # "DT4 8SA",
            # "DT5 2FD",
            # "DT5 2FB",
            # "DT6 3BG",
            # "DT7 3FB",
            # "DT7 3FA",
            # "SP7 8NW",
            # "DT4 7LF",
            # "DT4 7LE",
            # "DT4 7LA",
            # "DT4 7LN",
            # "BH21 7BN",
        ]:
            return None

        if (
            uprn
            in [
                # "100041048946",  # 21A EAST STREET, CORFE CASTLE, WAREHAM
                # "10013297602",  # FLAT, 30A SALISBURY STREET, BLANDFORD FORUM
                # "200004827925",  # SLEPE HOUSE, ARNE, WAREHAM
                # "10011954350",  # ICEN BARN, GRANGE ROAD, WAREHAM
                # "100041099139",  # THE DOVE HOUSE, GRANGE ROAD, WAREHAM
                # "100040659908",  # 64 BUXTON ROAD, WEYMOUTH
                # "100040673515",  # 77 RODWELL ROAD, WEYMOUTH
                # "200000754050",  # 25 COLDHARBOUR, CHICKERELL, WEYMOUTH
                # "200001871356",  # BRACKEN COTTAGE, EAST BURTON ROAD, WOOL, WAREHAM
                # "100041231992",  # THE COURTYARD CRAFT CENTRE, HUNTICK ROAD, LYTCHETT MINSTER, POOLE
                # "10023242607",  # LITTLE RIDGE, WATERSTON, DORCHESTER
                # "200000750217",  # HAZYVIEW, RYALL ROAD, RYALL, BRIDPORT
                # "200000767496",  # EAST BARN, WOOTTON FITZPAINE, BRIDPORT
                # "200000767497",  # WEST BARN, WOOTTON FITZPAINE, BRIDPORT
                # "10002641794",  # STATION LODGE, HOLYWELL, DORCHESTER
                # "10071152307",  # POPPY BANK FARM HIGHER STREET, OKEFORD FITZPAINE
                # "200004818260",  # THE WHITE HOUSE DOREYS FARM ACCESS ROAD TO NEW HALL FARM, WAREHAM
            ]
        ):
            return None

        return super().address_record_to_dict(record)
