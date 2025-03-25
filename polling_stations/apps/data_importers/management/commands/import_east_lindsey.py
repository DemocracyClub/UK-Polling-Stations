from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ELI"
    addresses_name = (
        "2025-05-01/2025-03-25T10:23:40.621530/ELDC - Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-25T10:23:40.621530/ELDC - Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # more accurate point for: St Marys Church, Church Lane, Fotherby, Louth, LN11 0UJ
        if record.polling_place_id == "12564":
            record = record._replace(polling_place_easting="531703")
            record = record._replace(polling_place_northing="391688")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200001828818",  # GRANGE FARM, WELTON-LE-MARSH, SPILSBY
            "10024297692",  # LAKE VIEW STATION ROAD, LITTLE STEEPING
            "100032167500",  # WINDSOR COTTAGE, HAKERLEY BRIDGE, FRITHVILLE, BOSTON
            "10090638895",  # THE PADDOCKS, CROFT LANE, CROFT, SKEGNESS
            "100032166988",  # STONEY BROKE, TRADER BANK, SIBSEY, BOSTON
            "10008523556",  # JASMINE LODGE, MAIN ROAD, SIBSEY, BOSTON
            "10008523556",  # A97 MERMAID CARAVAN PARK SEAHOLME ROAD, MABLETHORPE
            "10093437401",  # A37 MERMAID CARAVAN PARK SEAHOLME ROAD, MABLETHORPE
        ]:
            return None

        if record.addressline6 in [
            # splits
            "PE25 2PX",
            "PE24 5UT",
            "LN8 5LR",
            "LN12 2HX",
            "LN9 5JP",
            "LN11 0EG",
            # looks wrong
            "PE25 2FE",
        ]:
            return None

        return super().address_record_to_dict(record)
