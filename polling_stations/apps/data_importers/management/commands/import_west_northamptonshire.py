from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WNT"
    addresses_name = (
        "2025-05-01/2025-03-24T13:37:27.991423/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-24T13:37:27.991423/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "28017243",  # WOODYARD COTTAGE, WATLING STREET, WEEDON, NORTHAMPTON
            "15076305",  # OLD LODGE, LONDON ROAD, COLLINGTREE, NORTHAMPTON
            "15054454",  # 105 ST. ANDREWS ROAD, NORTHAMPTON
            "15126528",  # 103B ST. ANDREWS ROAD, NORTHAMPTON
            "15089445",  # 103A ST, ANDREWS ROAD, NORTHAMPTON
            "28047695",  # WESTCOMBE FARM, FAWSLEY, DAVENTRY
            "28021613",  # SYBOLE FARM, SOUTH KILWORTH ROAD, WELFORD, NORTHAMPTON
            "200001816977",  # PEAS FURLONG COTTAGE, CULWORTH, BANBURY
            "200001471831",  # CORNERS, BANBURY LANE, FOSTERS BOOTH, TOWCESTER
            "10023964831",  # 2 BANBURY LANE, FOSTERS BOOTH, TOWCESTER
            "10023963398",  # ANNEXE WOODEND GRANGE ROAD TO HINTON AIRFIELD, NEWBOTTLE
            "10000459924",  # WOODEND GRANGE, STEANE, BRACKLEY
            "10000462912",  # HINTON GROUNDS FARM, HINTON-IN-THE-HEDGES, BRACKLEY
            "10013086563",  # BRACKLEY GORSE, BRACKLEY GORSE, BANBURY ROAD, BRACKLEY
        ]:
            return None

        if record.addressline6 in [
            # splits
            "NN12 6RN",
            "NN3 7AY",
            "NN2 6LD",
            "NN2 7EL",
            "NN6 9HG",
            "NN11 6YH",
            # looks wrong
            "NN3 8NU",
            "NN7 4LB",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # point correction for: Mobile Unit, Local Centre Car Park, Bordeaux Close, Off Weggs Farm Road, Alsace Park, Northampton, NN5 6YR
        if record.polling_place_id == "45023":
            record = record._replace(polling_place_easting="470877")
            record = record._replace(polling_place_northing="262278")

        # add missing postcode for: Tove Valley Centre, Northampton Road, Towcester
        if record.polling_place_id == "45574":
            record = record._replace(polling_place_postcode="NN12 7AH")

        # remove wrong point for: Mobile Unit, Sunnyside Public House, Boughton Green Road, Northampton, NN2 7AG (bug report 761)
        if record.polling_place_id == "45193":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        return super().station_record_to_dict(record)
