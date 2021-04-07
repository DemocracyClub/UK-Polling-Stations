from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ELI"
    addresses_name = "2021-03-29T14:54:03.784744/Democracy_Club__06May2021.csv"
    stations_name = "2021-03-29T14:54:03.784744/Democracy_Club__06May2021.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        # St Marys Church Church Lane Fotherby Louth
        if record.polling_place_id == "9064":
            record = record._replace(polling_place_easting="531703")
            record = record._replace(polling_place_northing="391688")

        # Church Institute Church Lane South Elkington LN11 OSA
        if record.polling_place_id == "9060":
            record = record._replace(polling_place_postcode="LN11 0SA")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10008528388":  # AMERICA FARM, HANNAH, ALFORD
            record = record._replace(addressline6="LN13 9QP")

        if uprn in [
            "100030775814",  # SEA SHADOW, CHURCHILL LANE, THEDDLETHORPE, MABLETHORPE
            "200001828818",  # GRANGE FARM, WELTON-LE-MARSH, SPILSBY
            "10024297692",  # LAKE VIEW STATION ROAD, LITTLE STEEPING
            "100032167500",  # WINDSOR COTTAGE, HAKERLEY BRIDGE, FRITHVILLE, BOSTON
            "200002780835",  # BARBRIDGE HOUSE, MAIN ROAD, SIBSEY, BOSTON
            "100030754138",  # NORTHERN LODGE, MAIN ROAD, SIBSEY, BOSTON
        ]:
            return None

        if record.addressline6 in [
            "PE24 5RE",
            "PE24 5UT",
            "LN9 5JP",
            "LN11 0EG",
            "LN11 8DW",
            "LN12 2HX",
            "PE25 2PX",
            "PE25 3BS",
            "PE22 8DQ",
            "PE25 1SH",
        ]:
            return None

        return super().address_record_to_dict(record)
