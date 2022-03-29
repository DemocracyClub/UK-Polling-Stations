from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BST"
    addresses_name = (
        "2022-05-05/2022-03-23T12:04:30.972191/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-23T12:04:30.972191/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.post_code in ["BS2 9LP"]:
            return None  # split

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # St Anne`s Infants School Community Room Bloomfield Road Brislington Bristol BS4 4EJ
        if record.polling_place_id == "17540":
            record = record._replace(polling_place_postcode="BS4 3QJ")

        # Southmead Community Centre, 248 Greystoke Avenue, Bristol
        if record.polling_place_id == "17953":
            record = record._replace(polling_place_postcode="BS10 6BQ")

        return super().station_record_to_dict(record)
