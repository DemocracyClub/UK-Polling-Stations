from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "OLD"
    addresses_name = "2021-03-25T12:33:04.363809/Oldham Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-25T12:33:04.363809/Oldham Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # The Childrens Centre, Higher Failsworth Primary School, Stansfield Road, Failsworth
        if record.polling_place_id == "7352":
            record = record._replace(polling_place_postcode="")
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.148726, 53.514296, srid=4326)
            return rec

        # Mather Street Primary School Mather Street Failsworth Manchester M35 ODT
        if record.polling_place_id == "7364":
            record = record._replace(polling_place_postcode="M35 0DT")

        # Springhead Football Club Off St John Street Lees Oldham OL4 3DG
        if record.polling_place_id == "7566":
            record = record._replace(polling_place_postcode="OL4 3DR")

        # Coldhurst Lifelong Learning Centre Rochdale Road Oldham OL1 2JD
        if record.polling_place_id == "7307":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "422000098508",  # WHITFIELD COTTAGE, WHITFIELD, SHAW, OLDHAM
            "422000120354",  # FLAT 3 THE BUNGALOW 43 GRAINS ROAD, DELPH
            "422000060807",  # DOLEFIELD BARN, FUR LANE, GREENFIELD, OLDHAM
            "422000120352",  # FLAT 1 THE BUNGALOW 43 GRAINS ROAD, DELPH
            "422000129256",  # 14 MANCHESTER ROAD, GREENFIELD, OLDHAM
            "422000119217",  # 1 FITTON STREET, ROYTON, OLDHAM
            "422000129521",  # 237 COALSHAW GREEN ROAD, CHADDERTON, OLDHAM
            "422000120353",  # FLAT 2 THE BUNGALOW 43 GRAINS ROAD, DELPH
            "422000125257",  # 80 EUSTACE STREET, CHADDERTON, OLDHAM
            "422000014564",  # 81 DERBY STREET, CHADDERTON, OLDHAM
            "422000046320",  # 40 TANDLEWOOD PARK, ROYTON, OLDHAM
            "422000034427",  # 66 ROMAN ROAD, FAILSWORTH, MANCHESTER
            "422000120355",  # FLAT 4 THE BUNGALOW 43 GRAINS ROAD, DELPH
            "100011199092",  # 144 BROADWAY, ROYTON, OLDHAM
            "422000102588",  # FLAT 2 76-78 MILNROW ROAD, SHAW
            "422000125258",  # 82 EUSTACE STREET, CHADDERTON, OLDHAM
            "422000102589",  # FLAT 1 76-78 MILNROW ROAD, SHAW
            "422000120408",  # VALE COTTAGE, STANDEDGE, DELPH, OLDHAM
            "422000069004",  # 3 STATION LANE, GREENFIELD, OLDHAM
            "422000061537",  # 81 OLDHAM ROAD, GRASSCROFT, OLDHAM
            "422000124671",  # 239 OLDHAM ROAD, SPRINGHEAD, OLDHAM
            "422000064639",  # 2 STONEBOTTOM BROW, DOBCROSS, OLDHAM
            "422000126990",  # 556B CHAMBER ROAD, OLDHAM
            "422000036274",  # 2 SCHOLES STREET, FAILSWORTH, MANCHESTER
            "422000129006",  # 189B OLDHAM ROAD, SPRINGHEAD, OLDHAM
            "100011199050",  # 109 BROADWAY, ROYTON, OLDHAM
            "422000014571",  # 91 DERBY STREET, CHADDERTON, OLDHAM
            "422000112010",  # TURNING POINT BIRCHWOOD, BIRCHWOOD NURSING HOME, LEES NEW ROAD, OLDHAM
            "100011210768",  # 83 DERBY STREET, OLDHAM
            "422000130564",  # INTAKE FARM STANDEDGE HUDDERSFIELD ROAD, DELPH
            "422000112176",  # BENTLEY FARM, STANDEDGE, DELPH, OLDHAM
            "422000112170",  # MANOR HOUSE FARM, STANDEDGE, DELPH, OLDHAM
            "422000112177",  # STANDEDGE FOOT FARM, STANDEDGE, DELPH, OLDHAM
            "422000113798",  # 1 NEAR SPRINGS, STANDEDGE, DELPH, OLDHAM
            "422000119510",  # FALCONERS ARMS HOLLINS ROAD, OLDHAM
            "422000065012",  # LOWER SLACK, SLACKGATE LANE, DENSHAW, OLDHAM
            "422000066942",  # 2 COOPER STREET, SPRINGHEAD, OLDHAM
        ]:
            return None

        if record.addressline6 in [
            "OL4 4SD",
            "OL8 3SF",
            "OL8 1DX",
            "OL4 4SB",
            "OL2 8DT",
            "OL4 3PA",
            "M35 0TN",
            "OL3 5BG",
            "OL1 4NT",
            "OL2 8HS",
            "OL2 8TN",
            "OL2 8DF",
            "M35 9JU",
            "OL8 3PE",
            "OL9 6BB",
            "OL8 2NE",
            "OL8 1DD",
            "OL8 2BA",
        ]:
            return None

        if "Moorlea Evening Street" in record.addressline1:
            return None

        return super().address_record_to_dict(record)
