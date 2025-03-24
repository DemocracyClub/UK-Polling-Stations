from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SGC"
    addresses_name = (
        "2025-05-01/2025-03-24T13:48:42.656093/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-24T13:48:42.656093/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "689538",  # THE ANNEXE HAM FARM COTTAGE EMERSONS GREEN LANE, EMERSONS GREEN
            "546172",  # HAM FARM COTTAGE, EMERSONS GREEN LANE, EMERSONS GREEN, BRISTOL
            "690417",  # LOVELL PLACE, SPARROWBILL WAY, PATCHWAY, BRISTOL
            "694291",  # 40A CONYGRE GROVE, FILTON, BRISTOL
            "537010",  # 5 LYTCHET DRIVE, Bristol
            "572571",  # 101 HICKS COMMON ROAD, WINTERBOURNE, BRISTOL
            "575251",  # 1 GREEN LANE, CUTTS HEATH, WOTTON-UNDER-EDGE
            "648304",  # 2 GREEN LANE, CUTTS HEATH, WOTTON-UNDER-EDGE
        ]:
            return None
        if record.addressline6 in [
            # split
            "BS37 6DF",
            "BS15 3HW",
            "BS16 1RR",
            "BS15 3HP",
            "BS30 5TP",
            "BS32 4AH",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # correct location for: Trust Hall-Stoke Gifford, North Road, Stoke Gifford, Bristol, BS34 8PE
        if record.polling_place_id == "18009":
            record = record._replace(
                polling_place_easting="362576",
                polling_place_northing="179880",
                polling_place_uprn="",
            )
        return super().station_record_to_dict(record)
