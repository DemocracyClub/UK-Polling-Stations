from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COT"
    addresses_name = "2021-03-05T09:20:27.484157/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-05T09:20:27.484157/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10023475981",  # SELWORTHY, MORETON ROAD, STOW ON THE WOLD, CHELTENHAM
            "10013878640",  # BARTON MEADOW LODGE, GUITING POWER, CHELTENHAM
            "10093270137",  # WOODLAND BARN FARM, WHITEWAY, CIRENCESTER
            "10013883455",  # BURGAGE END FARMINGTON ROAD, NORTHLEACH
        ]:
            return None

        if record.addressline6 in [
            "GL8 8SQ",
            "GL7 7EX",
            "GL7 7BA",
        ]:
            return None

        return super().address_record_to_dict(record)
