from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BST"
    addresses_name = "2021-03-24T17:38:12.449323/bristol_deduped.tsv"
    stations_name = "2021-03-24T17:38:12.449323/bristol_deduped.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.post_code in ["BS6 7AT"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # St Anne`s Infants School Community Room Bloomfield Road Brislington Bristol BS4 4EJ
        if record.polling_place_id == "12587":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
