from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COT"
    addresses_name = "2021-02-23T13:29:42.051423/Democracy_Club__06May2021.tsv"
    stations_name = "2021-02-23T13:29:42.051423/Democracy_Club__06May2021.tsv"
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

    def station_record_to_dict(self, record):

        # source: https://britishlistedbuildings.co.uk/101340859-village-hall-icomb
        # Icomb Village Hall
        if record.polling_place_id == "17236":
            record = record._replace(polling_place_northing="222640")

        return super().station_record_to_dict(record)
