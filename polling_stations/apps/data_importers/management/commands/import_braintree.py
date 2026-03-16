from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRA"
    addresses_name = (
        "2026-05-07/2026-03-16T13:19:41.945873/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-16T13:19:41.945873/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
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
                "10095522114",  # BURFORDS, HAVERHILL ROAD, HELIONS BUMPSTEAD, HAVERHILL
            ]
        ):
            return None

        if record.post_code in [
            # splits
            "CM7 1XX",
            "CM8 1HS",
            "CM7 4QH",
            # supect
            "CM7 3JW",
            "CM7 3JJ",
            "CO9 4QS",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # location correction for: Witham Public Hall, Collingwood Road, Witham, CM8 1EU
        if rec["internal_council_id"] == "11561":
            rec["location"] = Point(0.6392043768856295, 51.80161589272421, srid=4326)

        return rec
