from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ELI"
    addresses_name = (
        "2024-05-02/2024-03-21T11:00:56.741087/Democracy_Club__02May2024 (20) (1).tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-21T11:00:56.741087/Democracy_Club__02May2024 (20) (1).tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # more accurate point for: St Marys Church, Church Lane, Fotherby, Louth, LN11 0UJ
        if record.polling_place_id == "11523":
            record = record._replace(polling_place_easting="531703")
            record = record._replace(polling_place_northing="391688")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200001828818",  # GRANGE FARM, WELTON-LE-MARSH, SPILSBY
            "10024297692",  # LAKE VIEW STATION ROAD, LITTLE STEEPING
            "100032167500",  # WINDSOR COTTAGE, HAKERLEY BRIDGE, FRITHVILLE, BOSTON
            "100032077624",  # EVENWOOD, FIRE BEACON LANE, COVENHAM ST. BARTHOLOMEW, LOUTH
            "100032260114",  # FIREBEACON BRIDGE FARM, FIREBEACON LANE, WRAGHOLME, LOUTH
            "10090638895",  # THE PADDOCKS, CROFT LANE, CROFT, SKEGNESS
            "100032166988",  # STONEY BROKE, TRADER BANK, SIBSEY, BOSTON
            "10008523556",  # JASMINE LODGE, MAIN ROAD, SIBSEY, BOSTON
            "10096344217",  # A97 MERMAID CARAVAN PARK SEAHOLME ROAD, MABLETHORPE
            "10093437401",  # A37 MERMAID CARAVAN PARK SEAHOLME ROAD, MABLETHORPE
            "10008514781",  # DUDDLES FARM, SANDY BANK, NEW YORK, LINCOLN
            "10008521252",  # CORNFIELDS, LITTLE CARLTON, LOUTH
            "10094011546",  # FOXHALL, PARK ROW, LOUTH
        ]:
            return None

        if record.addressline6 in [
            # splits
            "LN11 8QG",
            "LN11 8DW",
            "LN9 5JP",
            "PE25 2PX",
            "LN8 5LR",
            "LN11 0EG",
            "PE24 5UT",
            "LN12 2HX",
            # looks wrong
            "PE25 2FE",
        ]:
            return None

        return super().address_record_to_dict(record)
