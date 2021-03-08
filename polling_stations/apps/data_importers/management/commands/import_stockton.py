from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STT"
    addresses_name = "2021-03-08T13:26:49.693904/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-08T13:26:49.693904/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in ["TS18 3EF", "TS20 2TJ", "TS17 9PA"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if (
            record.polling_place_id == "12442"
        ):  # Kirklevington & Castlelevington Memorial Hall Pump Lane Kirklevington Yarm
            record = record._replace(polling_place_postcode="TS15 9LQ")

        if (
            record.polling_place_id == "12555"
        ):  # Elim Pentecostal Church Ragpath Lane Roseworth Stockton on Tees
            record = record._replace(polling_place_postcode="TS19 9AT")

        if (
            record.polling_place_id == "12408"
        ):  # North Billingham Methodist Church Activity Room - rear of the Church Marsh House Avenue Billingham TS23 3TG
            record = record._replace(polling_place_postcode="TS23 3ET")

        if (
            record.polling_place_id == "12409"
        ):  # North Billingham Methodist Church Front Door Marsh House Avenue Billingham TS23 3TG
            record = record._replace(polling_place_postcode="TS23 3ET")

        if (
            record.polling_place_id == "12599"
        ):  # Oxbridge Christian Fellowship The Apostolic Church Main Entrance 65 Oxbridge Lane Stockton-on-Tees TS18 4DN (copied postcode from address row to postcode row)
            record = record._replace(polling_place_postcode="TS18 4DN")

        if (
            record.polling_place_id == "12648"
        ):  # Eltham Crescent Community Centre Eltham Crescent Thornaby Stockton-on-Tees
            record = record._replace(polling_place_postcode="TS17 9RG")

        return super().station_record_to_dict(record)
