from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHO"
    addresses_name = (
        "2021-04-16T14:09:22.768202/S Holland Democracy_Club__06May2021.tsv"
    )
    stations_name = "2021-04-16T14:09:22.768202/S Holland Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100030894500",  # BUSLEY, SOUTH DROVE, SPALDING
            "100030888845",  # AMOW, MIDDLE MARSH ROAD, MOULTON MARSH, SPALDING
            "100030887883",  # 1 FARM COTTAGE, GEDNEY DYKE, SPALDING
            "100032311625",  # 2 FARM COTTAGE, GEDNEY DYKE, SPALDING
        ]:
            return None

        if record.addressline6 in [
            "PE12 8LT",
            "PE12 0BL",
            "PE12 8SE",
            "PE12 8BP",
            "PE6 0LR",
            "PE12 8EP",
            "PE12 0HY",
            "PE11 3TB",
            "PE11 3NB",
            "PE12 9QJ",
            "PE11 4JH",
            "PE12 0XA",
            "PE12 6SD",
            "PE12 6DN",
            "PE12 7FG",
            "PE12 0HZ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Scout & Guide Headquarters Park Lane Long Sutton Spalding PE12 9DH
        if record.polling_place_id == "3793":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
