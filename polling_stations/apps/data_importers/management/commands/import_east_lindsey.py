from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ELI"
    addresses_name = (
        "2023-05-04/2023-03-20T15:39:49.119114/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-20T15:39:49.119114/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        #  Multi Purpose Room, Meridian Leisure Centre Wood Lane, Louth, Lincolnshire, LN11 8RA
        if record.polling_place_id == "9885":
            record = record._replace(polling_place_postcode="LN11 8SA")

        # St Marys Church, Church Lane, Fotherby, Louth, LN11 0UJ
        if record.polling_place_id == "9974":
            record = record._replace(polling_place_easting="531703")
            record = record._replace(polling_place_northing="391688")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200001828818",  # GRANGE FARM, WELTON-LE-MARSH, SPILSBY
            "10024297692",  # LAKE VIEW STATION ROAD, LITTLE STEEPING
            "100032167500",  # WINDSOR COTTAGE, HAKERLEY BRIDGE, FRITHVILLE, BOSTON
            "200002780835",  # BARBRIDGE HOUSE, MAIN ROAD, SIBSEY, BOSTON
            "100032077624",  # EVENWOOD, FIRE BEACON LANE, COVENHAM ST. BARTHOLOMEW, LOUTH
            "100032260114",  # FIREBEACON BRIDGE FARM, FIREBEACON LANE, WRAGHOLME, LOUTH
            "10090638895",  # THE PADDOCKS, CROFT LANE, CROFT, SKEGNESS
            "100032166988",  # STONEY BROKE, TRADER BANK, SIBSEY, BOSTON
            "10008523556",  # JASMINE LODGE, MAIN ROAD, SIBSEY, BOSTON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "LN11 0EG",
            "LN11 8QG",
            "LN9 5JP",
            "LN11 8DW",
            "LN12 2HX",
            "PE25 2PX",
            "PE24 5UT",
            "PE25 1SH",  # TILE HOUSE, ROSE GROVE, SKEGNESS
            "PE25 2BG",  # LEEMING DRIVE, SKEGNESS
            "PE25 2FD",  # RAY CLEMENCE WAY, SKEGNESS
            "PE22 7SL",  # STATION ROAD, TUMBY WOODSIDE, BOSTON
        ]:
            return None

        return super().address_record_to_dict(record)
