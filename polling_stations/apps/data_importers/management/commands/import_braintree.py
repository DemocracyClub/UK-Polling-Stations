from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRA"
    addresses_name = (
        "2023-05-04/2023-03-01T16:34:23.372357/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-01T16:34:23.372357/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10006916373",  # MAPLE HOUSE, STURMER ROAD, NEW ENGLAND, HALSTEAD
            "10006910392",  # EYSTON SMYTHS FARM, FOXEARTH, SUDBURY
            "100090317907",  # 55 LITTLE YELDHAM ROAD, GREAT YELDHAM, HALSTEAD
            "100090317908",  # 57 LITTLE YELDHAM ROAD, GREAT YELDHAM, HALSTEAD
            "10006929905",  # LITTLE CHELMSHOE HOUSE, GESTINGTHORPE ROAD, GREAT MAPLESTEAD, HALSTEAD
            "100091218537",  # SRINIVASA, ALDERFORD STREET, SIBLE HEDINGHAM, HALSTEAD
            "10006933344",  # 1 MOUNTS FARM SHALFORD ROAD, RAYNE
            "10006917987",  # GEORGE GARDENS, QUEENBOROUGH LANE, RAYNE, BRAINTREE
            "100091215988",  # PUDNEYS FARM, SHALFORD ROAD, RAYNE, BRAINTREE
            "10006925380",  # SPRINGLETTE, CORNISH HALL END, BRAINTREE
            "10090832495",  # FLAT ABOVE 3 BOCKING END, BRAINTREE
            "10090831818",  # 4A RAYNE ROAD, BRAINTREE
            "100091214154",  # NEW DIRECTION, DAVID BLACKWELL HOUSE 25-27, BOCKING END, BRAINTREE
            "100091452899",  # DENGIE FARMHOUSE, MALDON ROAD, WITHAM
            "10006912116",  # OLD THATCH, RAVENSHALL ROAD, GREENSTEAD GREEN, HALSTEAD
            "10006927838",  # MARSH COTTAGE, GOSFIELD ROAD, WETHERSFIELD, BRAINTREE
            "10006915800",  # PONYACRES, ROTTEN END, WETHERSFIELD, BRAINTREE
            "10006922317",  # SPAINS END FARM, CORNISH HALL END, BRAINTREE
        ]:
            return None

        if record.post_code in [
            # splits
            "CM7 1XX",
            "CM8 1HS",
            "CM7 4QH",
            "CO10 7DH",
            "CO6 1RS",
            "CO6 1RR",
            "CO6 1FH",
            "CM7 3JW",  # 6 - 96 EAST STREET, BRAINTREE
            "CM7 3JJ",  # 6 - 96 EAST STREET, BRAINTREE
            "CM3 2AQ",  # 1 WHITELANDS NEW COTTAGES, TERLING ROAD, HATFIELD PEVEREL, CHELMSFORD
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Panfield Village Hall, Panfield
        if record.polling_place_id == "9158":
            record = record._replace(polling_place_postcode="CM7 5AQ")

        rec = super().station_record_to_dict(record)

        # Witham Public Hall, Collingwood Road, Witham
        if rec["internal_council_id"] == "9230":
            rec["location"] = Point(0.6392043768856295, 51.80161589272421, srid=4326)

        return rec
