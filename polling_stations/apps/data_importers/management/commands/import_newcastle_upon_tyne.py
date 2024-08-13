from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NET"
    addresses_name = (
        "2024-07-04/2024-05-31T11:08:38.640289/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-31T11:08:38.640289/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "4510034357",  # LOUGH BRIDGE HOUSE, CALLERTON, NEWCASTLE UPON TYNE
                "4510044349",  # 11 ROKEBY AVENUE, NEWCASTLE UPON TYNE
                "4510044350",  # 12 ROKEBY AVENUE, NEWCASTLE UPON TYNE
                "4510014924",  # 34 DENTON AVENUE, NEWCASTLE UPON TYNE
                "4510095971",  # 2 WOODSTOCK ROAD, NEWCASTLE UPON TYNE
                "4510048289",  # 56 WOODSTOCK ROAD, NEWCASTLE UPON TYNE
                "4510755893",  # 63 WHITE HOUSE ROAD, NEWCASTLE UPON TYNE
                "4510001747",  # 53 CAROLINE STREET, NEWCASTLE UPON TYNE
                "4510106463",  # 2 CLIFFORD ROAD, NEWCASTLE UPON TYNE
                "4510755706",  # 633 WELBECK ROAD, NEWCASTLE UPON TYNE
                "4510083769",  # 278 FOSSWAY, NEWCASTLE UPON TYNE
                "4510116542",  # 515 SHIELDS ROAD, NEWCASTLE UPON TYNE
                "4510141284",  # P T E SOCIAL CLUB, MILLERS ROAD, NEWCASTLE UPON TYNE
                "4510116916",  # 5 STONEYHURST ROAD WEST, NEWCASTLE UPON TYNE
                "4510731041",  # FLAT, 6 ST. MARYS PLACE, NEWCASTLE UPON TYNE
                "4510728933",  # THE BUNGALOW EXHIBITION PARK CLAREMONT ROAD, NEWCASTLE UPON TYNE
                "4510007930",  # NORTH EAST LODGE, FREEMAN ROAD, HIGH HEATON, NEWCASTLE UPON TYNE
                "4510705708",  # NORTH EAST PUBLISHING, 415 CHILLINGHAM ROAD, NEWCASTLE UPON TYNE
                "4510759485",  # FLAT PTE SOCIAL CLUB MILLERS ROAD, NEWCASTLE UPON TYNE
                "4510093017",  # 113 SCROGG ROAD, NEWCASTLE UPON TYNE
                "4510729862",  # NEWCASTLE CITY COUNCIL, 45A SAINT PETERS ROAD, NEWCASTLE UPON TYNE
                "4510139277",  # ST. TERESA'S PRESBYTERY, HEATON ROAD, NEWCASTLE UPON TYNE
                "4510729862",  # NEWCASTLE CITY COUNCIL, 45A SAINT PETERS ROAD, NEWCASTLE UPON TYNE
                "4510068272",  # 4 FAIRHOLM ROAD, NEWCASTLE UPON TYNE
                "4510138279",  # BENWELL & DISTRICT SOCIAL CLUB, SPRINGBANK, CONDERCUM ROAD, NEWCASTLE UPON TYNE
                "4510017556",  # TRINITY ACADEMY NEWCASTLE, CONDERCUM ROAD, NEWCASTLE UPON TYNE
                "4510736476",  # 1 FEATHERWOOD AVENUE, NEWCASTLE UPON TYNE
                "4510736474",  # 17 FEATHERWOOD AVENUE, NEWCASTLE UPON TYNE
                "4510735849",  # 51 BELLSHIEL GROVE, NEWCASTLE UPON TYNE
                "4510735823",  # 40 CHESTER PIKE, NEWCASTLE UPON TYNE
                "4510746154",  # 241 ARMSTRONG ROAD, NEWCASTLE UPON TYNE
                "4510746161",  # 243 ARMSTRONG ROAD, NEWCASTLE UPON TYNE
                "4510755895",  # 1 CHESTERHOLM AVENUE, NEWCASTLE UPON TYNE
                "4510076689",  # 127 BENWELL LANE, NEWCASTLE UPON TYNE
                "4510096100",  # 1 YEWCROFT AVENUE, NEWCASTLE UPON TYNE
                "4510138207",  # KENTON HALL COTTAGE, KENTON LANE, NEWCASTLE UPON TYNE
                "4510044741",  # 1 THE RIDGEWAY, KENTON, NEWCASTLE UPON TYNE
                "4510074737",  # 13 BEECHFIELD ROAD, NEWCASTLE UPON TYNE
                "4510018255",  # 1 HEXHAM AVENUE, NEWCASTLE UPON TYNE
                "4510746160",  # 241 ARMSTRONG ROAD, NEWCASTLE UPON TYNE
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "NE5 1QF",
            "NE4 9NQ",
            "NE5 2AZ",
            # suspect
            "NE15 9FD",  # GOLDCREST ROAD, NEWCASTLE UPON TYNE
            "NE6 4AZ",  # HADRIANS DRIVE, NEWCASTLE UPON TYNE
            "NE5 2BR",  # SANDRINGHAM ROAD, EAST DENTON, NEWCASTLE UPON TYNE
            "NE7 7BQ",  # JESMOND DENE, NEWCASTLE UPON TYNE
            "NE3 2TL",  # BRUNTON WALK, NEWCASTLE UPON TYNE
            "NE6 1PT",  # BRIAN ROYCROFT COURT, BURTON STREET, NEWCASTLE UPON TYNE
            "NE15 6BU",  # ARMSTRONG ROAD, NEWCASTLE UPON TYNE
            "NE15 6EQ",  # WHITEHOUSE ROAD, NEWCASTLE UPON TYNE
            "NE15 6NZ",  # BEAMISH PLACE, NEWCASTLE UPON TYNE
            "NE15 6NW",  # GREEN TREE COURT, BENWELL VILLAGE, NEWCASTLE UPON TYNE
            "NE5 1NH",  # HILLHEAD FARM COTTAGE, HILLHEAD ROAD, NEWCASTLE UPON TYNE
            "NE3 5EQ",  # HEATHERY LANE COTTAGES, HEATHERY LANE, NEWCASTLE UPON TYNE
            "NE2 1DJ",  # PORTLAND ROAD, SHIELDFIELD, NEWCASTLE UPON TYNE
            "NE5 2FD",  # ALLENDALE COURT, NEWCASTLE UPON TYNE
        ]:
            return None  # split

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Council has asked us not to show polling station locations
        record = record._replace(
            polling_place_uprn="", polling_place_easting="", polling_place_northing=""
        )

        # All postcodes below are provided by the council:

        # St Aidan`s Community Centre, Princes Road, Brunton Park, Gosforth
        if record.polling_place_id == "15165":
            record = record._replace(polling_place_postcode="NE3 5NJ")

        # Throckley Community Hall, Back Victoria Terrace, Throckley, Newcastle upon Tyne, NE15 9EL
        if record.polling_place_id == "15188":
            record = record._replace(polling_place_postcode="NE15 9AA")

        # Westerhope Bowling Club, Bowls Recreation Pavilion, West Avenue, Newcastle upon Tyne, NE5 5JH
        if record.polling_place_id == "15286":
            record = record._replace(polling_place_postcode="NE5 2LL")

        # Blucher Methodist Church, Blucher Terrace, Newcastle upon Tyne, NE15 9SD
        if record.polling_place_id == "15328":
            record = record._replace(polling_place_postcode="NE15 9SH")

        # St James` and St Basil`s Church Hall, Wingrove Road North, Fenham, Newcastle upon Tyne, NE4 9UB
        if record.polling_place_id == "15361":
            record = record._replace(polling_place_postcode="NE4 9EJ")

        # Station address: 'Trinity Community Centre, Freeman Road, Newcastle upon Tyne, NE3 1SS
        if record.polling_place_id == "15096":
            record = record._replace(polling_place_postcode="NE3 1SX")

        # Heaton Baptist Church, Heaton Road, Mundella Terrace, Heaton, NE6 5HN
        # Postcode is correct

        # Church of the Ascension Church Hall, Creighton Avenue, Newcastle upon Tyne, NE3 4UN
        # Postcode is correct

        # West Gosforth Scout Group, Brookvale Avenue, Newcastle upon Tyne, NE3 4JX
        # Postcode is correct

        return super().station_record_to_dict(record)
