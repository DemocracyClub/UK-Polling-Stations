from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DST"
    addresses_name = (
        "2024-05-02/2024-02-26T14:55:22.566450/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-26T14:55:22.566450/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # 'Beaminster Public Hall, 8 Fleet Street, Beaminster, DT8 3EF'
        if record.polling_place_id == "54992":
            record = record._replace(polling_place_uprn="10023243684")

        # 'Sutton Waldron Village Hall, The Street, Sutton Waldron, Blandford Forum, DT11 8NZ'
        if record.polling_place_id == "54978":
            record = record._replace(polling_place_postcode="DT11 8PB")

        # 'Colehill Village Hall - Station 1, Cannon Hill Road, Colehill, Wimborne, BH21 2LS'
        if record.polling_place_id == "55195":
            record = record._replace(polling_place_postcode="BH21 2LR")

        # 'Colehill Village Hall - Station 2, Cannon Hill Road, Colehill, Wimborne, BH21 2LS'
        if record.polling_place_id == "55201":
            record = record._replace(polling_place_postcode="BH21 2LR")

        # 'Colehill Village Hall - Station 3, Cannon Hill Road, Colehill, Wimborne, BH21 2LS'
        if record.polling_place_id == "55202":
            record = record._replace(polling_place_postcode="BH21 2LR")

        # 'Edmondsham Village Hall, Edmondsham, Wimborne, BH21 5RE'
        if record.polling_place_id == "55225":
            record = record._replace(polling_place_postcode="BH21 5RG")

        # 'St Mary the Virgin CE Primary School, Pheasant Way, Gillingham, SP8 4LP'
        if record.polling_place_id == "55421":
            record = record._replace(polling_place_postcode="SP8 4GG")

        # '***NEW LOCATION***Compass Terrace, Atlantic Academy, Maritime House, Southwell Park, Portland, DT5 2NA'
        if record.polling_place_id == "55578":
            record = record._replace(polling_place_postcode="DT5 2NP")

        # 'Puddletown Village Hall, High Street, DT2 8RY'
        if record.polling_place_id == "55585":
            record = record._replace(polling_place_postcode="DT2 8RX")

        # 'Milton Abbas Reading Room, Milton Abbas, Blandford Forum, DT11 0BW'
        if record.polling_place_id == "55595":
            record = record._replace(polling_place_postcode="DT11 0BN")

        # 'Winterborne Kingston Village Hall, West Street, Winterborne Kingston, DT11 9AX'
        if record.polling_place_id == "55599":
            record = record._replace(polling_place_postcode="DT11 9AZ")

        # 'All Saints Church Hall, 5 Redcliffe Road, Swanage, BH19 1LZ'
        if record.polling_place_id == "55803":
            record = record._replace(polling_place_postcode="BH19 1LL")

        # 'Hinton St Mary Village Hall, Hinton St Mary, Hinton St Mary, Sturminster Newton, DT10 1NB'
        if record.polling_place_id == "55799":
            record = record._replace(polling_place_postcode="DT10 1NA")

        # Station change from council:
        # old station: Weston Community Hall, Weston Road, Portland, DT5 2BZ (UPRN: 100041049367)
        # new station: Kimberlin Club, Blacknor Road, Portland, DT5 2HU (UPRN: 100041120927)
        if record.polling_place_id == "55571":
            record = record._replace(
                polling_place_uprn="100041120927",
                polling_place_name="Kimberlin Club",
                polling_place_address_1="Blacknor Road",
                polling_place_postcode="DT5 2HU",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6.strip() in [
            # split
            "BH16 6NE",
            "DT2 8DX",
            "BH21 2SJ",
            "SP8 4FS",
            "BH31 7BS",
            "SP7 8RE",
            "DT3 4DF",
            "DT4 7QN",
            "DT10 1QZ",
            "BH21 2PQ",
            "BH21 4AD",
            "BH24 2LX",
            "DT3 5FF",
            "SP8 4DG",
            "BH20 4BJ",
            "BH31 6PA",
            "BH24 2SL",
            "BH19 2PG",
            "DT2 7AP",
            "DT10 1HG",
            "DT10 1JQ",
            "BH21 7BG",
            "BH21 5NP",
            "BH20 5JJ",
            "DT3 6SD",
            # suspect
            "BH19 1DQ",
            "BH19 1BS",
            "BH19 1LD",
            "DT4 8SA",
            "DT5 2FD",
            "DT5 2FB",
            "DT6 3BG",
            "DT7 3FB",
            "DT7 3FA",
            "SP7 8NW",
            "DT4 7LF",
            "DT4 7LE",
            "DT4 7LA",
            "DT4 7LN",
            "BH21 7BN",
        ]:
            return None

        if uprn in [
            "100041048946",  # 21A EAST STREET, CORFE CASTLE, WAREHAM
            "10013297602",  # FLAT, 30A SALISBURY STREET, BLANDFORD FORUM
            "200004827925",  # SLEPE HOUSE, ARNE, WAREHAM
            "10011954350",  # ICEN BARN, GRANGE ROAD, WAREHAM
            "100041099139",  # THE DOVE HOUSE, GRANGE ROAD, WAREHAM
            "100040659908",  # 64 BUXTON ROAD, WEYMOUTH
            "100040673515",  # 77 RODWELL ROAD, WEYMOUTH
            "200000754050",  # 25 COLDHARBOUR, CHICKERELL, WEYMOUTH
            "200001871356",  # BRACKEN COTTAGE, EAST BURTON ROAD, WOOL, WAREHAM
            "100041231992",  # THE COURTYARD CRAFT CENTRE, HUNTICK ROAD, LYTCHETT MINSTER, POOLE
            "10023242607",  # LITTLE RIDGE, WATERSTON, DORCHESTER
            "200000750217",  # HAZYVIEW, RYALL ROAD, RYALL, BRIDPORT
            "200000767496",  # EAST BARN, WOOTTON FITZPAINE, BRIDPORT
            "200000767497",  # WEST BARN, WOOTTON FITZPAINE, BRIDPORT
            "10002641794",  # STATION LODGE, HOLYWELL, DORCHESTER
            "10071152307",  # POPPY BANK FARM HIGHER STREET, OKEFORD FITZPAINE
        ]:
            return None

        return super().address_record_to_dict(record)
