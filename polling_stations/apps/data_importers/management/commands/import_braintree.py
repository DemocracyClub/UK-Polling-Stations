from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRA"
    addresses_name = (
        "2024-07-04/2024-06-10T10:50:28.559545/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-10T10:50:28.559545/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10006910392",  # EYSTON SMYTHS FARM, FOXEARTH, SUDBURY
            "10006929905",  # LITTLE CHELMSHOE HOUSE, GESTINGTHORPE ROAD, GREAT MAPLESTEAD, HALSTEAD
            "10095523024",  # ANNEXE AT SRINIVASA ALDERFORD STREET, SIBLE HEDINGHAM
            "10006917987",  # GEORGE GARDENS, QUEENBOROUGH LANE, RAYNE, BRAINTREE
            "10090832495",  # FLAT ABOVE 3 BOCKING END, BRAINTREE
            "10090831818",  # 4A RAYNE ROAD, BRAINTREE
            "100091214154",  # NEW DIRECTION, DAVID BLACKWELL HOUSE 25-27, BOCKING END, BRAINTREE
            "100091451706",  # 23 BOCKING END, BRAINTREE
            "100091452899",  # DENGIE FARMHOUSE, MALDON ROAD, WITHAM
            "10006912116",  # OLD THATCH, RAVENSHALL ROAD, GREENSTEAD GREEN, HALSTEAD
            "10006927838",  # MARSH COTTAGE, GOSFIELD ROAD, WETHERSFIELD, BRAINTREE
            "10006915800",  # PONYACRES, ROTTEN END, WETHERSFIELD, BRAINTREE
            "10006922317",  # SPAINS END FARM, CORNISH HALL END, BRAINTREE
            "10095521841",  # 16 OTTER VALE, WITHAM
            "10095522116",  # BURGHLEY HOUSE, HAVERHILL ROAD, HELIONS BUMPSTEAD, HAVERHILL
            "10095521507",  # 12 LAXTON LANE, CRESSING, BRAINTREE
        ]:
            return None

        if record.post_code in [
            # splits
            "CM7 4QH",
            "CM8 1HS",
            "CM7 1XX",
            "CO10 7DH",
            # supect
            "CM7 3JW",  # 6 - 96 EAST STREET, BRAINTREE
            "CM7 3JJ",  # 6 - 96 EAST STREET, BRAINTREE
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # Witham Public Hall, Collingwood Road, Witham
        if rec["internal_council_id"] == "10693":
            rec["location"] = Point(0.6392043768856295, 51.80161589272421, srid=4326)

        return rec
