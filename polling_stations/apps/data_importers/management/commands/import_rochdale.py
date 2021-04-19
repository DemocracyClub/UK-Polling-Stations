from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RCH"
    addresses_name = "2021-03-29T14:37:17.929311/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-29T14:37:17.929311/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # The Coach House Victoria Street Littleborough Rochdale
        if record.polling_place_id == "3980":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.0961003, 53.6444469, srid=4326)
            return rec

        if record.polling_place_id in [
            "3919",  # Function Room At Lancashire Fold Pub Kirkway Middleton Manchester M24 4AA
            "3880",  # St Paul`s Parish Hall Black Pits Road Rochdale OL11 5TD
            "3820",  # Mobile Unit at the Black Dog Pub Corner of Rooley Moor Road and Ings Lane Rochdale OL12 6JZ
            "3797",  # Room At Rear of St James Church Off Thornham Lane Rochdale OL12 6UW
            "3809",  # Bowls Pavilion Chesham Gardens Rochdale OL11 2YB
        ]:
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "23109323",  # FIRST FLOOR FLAT 11A SPRING GARDENS, MIDDLETON
            "10023364069",  # 3 LODGE STREET, MIDDLETON, MANCHESTER
            "10023364206",  # 16A LODGE STREET, MIDDLETON, MANCHESTER
            "23016631",  # DANE HOUSE, WILLIAM STREET, MIDDLETON, MANCHESTER
            "23101081",  # LANGFIELD CARE HOME, WOOD STREET, MIDDLETON, MANCHESTER
            "23003824",  # 268 WOOD STREET, MIDDLETON, MANCHESTER
            "23003825",  # 270 WOOD STREET, MIDDLETON, MANCHESTER
            "23004543",  # LANGLEY LANE FARM, LANGLEY LANE, MIDDLETON, MANCHESTER
            "23100322",  # THE CARETAKERS HOUSE HOPWOOD HALL CAMPUS ROCHDALE ROAD, MIDDLETON
            "23013254",  # 270 GREEN LANE, HEYWOOD
            "23100354",  # 117A ROCHDALE ROAD EAST, HEYWOOD
            "23050342",  # 2 CHADWICK STREET, FIRGROVE, ROCHDALE
            "10090920156",  # 898 MANCHESTER ROAD, ROCHDALE
            "23108014",  # 1 CLOVERBANK, CLOVER STREET, ROCHDALE
            "23081457",  # 5 BRIDGE STREET, MILNROW, ROCHDALE
            "23070569",  # 8 BUCKLEY STREET, ROCHDALE
            "23093510",  # 11 TRAFALGAR STREET, ROCHDALE
            "23111927",  # FLAT 1 2 INDUSTRY STREET, LITTLEBOROUGH
            "23111928",  # FLAT 2 2 INDUSTRY STREET, LITTLEBOROUGH
            "23078246",  # ASHBROOK NEURO REHABILITATION, KITTER STREET, ROCHDALE
            "23090575",  # 3 FLETCHERS PASSAGE, CALDERBROOK ROAD, LITTLEBOROUGH
            "10090922501",  # MIDDLE WICKEN VIEW 2 WICKEN VIEW TODMORDEN ROAD, LITTLEBOROUGH
            "10090922502",  # 3 LOWER WICKEN VIEW, TODMORDEN ROAD, LITTLEBOROUGH
            "10023363964",  # 6 BELFIELD LANE, ROCHDALE
            "23098412",  # KATELEE HOUSE PENNINE FISHERIES TROUT FARM CALDERBROOK ROAD, LITTLEBOROUGH
            "23105172",  # PENNINE TROUT FARM & FISHERY, CALDERBROOK ROAD, LITTLEBOROUGH
        ]:
            return None

        if record.addressline6 in [
            "OL16 4SP",
            "OL12 0PX",
            "OL16 2SJ",
            "OL11 1LZ",
            "OL16 1FD",
            "OL16 4RF",
            "OL16 4QG",
            "OL12 7LF",
            "OL16 2NU",
            "OL16 3AU",
            "OL11 3AE",
            "OL16 2LJ",
            "OL10 3LW",
            "OL16 2SD",
            "M24 2SA",
            "OL12 0EG",
            "OL10 4DG",
            "OL10 3PH",
            "OL11 5TR",
            "OL11 5PP",
            "OL11 5PN",
            "OL10 3BJ",
            "OL10 3EJ",
            "OL16 2TH",
            "OL10 1FH",
            "M24 1LG",
            "OL12 7QE",
            "M24 2JZ",
            "M24 5EE",
            "M24 5UJ",
            "M24 5LU",
            "M24 2EU",
            "OL15 9JX",
            "OL15 9LY",
            "M24 6DW",
            "M24 2PR",
            "M24 4FJ",
            "OL15 0AP",
            "OL15 0JH",
            "M24 5TN",
            "OL10 4HF",
            "OL11 5BN",
            "OL11 2WE",
            "OL11 1AT",
        ]:
            return None

        return super().address_record_to_dict(record)
