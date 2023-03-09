from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BUR"
    addresses_name = (
        "2023-05-04/2023-03-09T16:44:01.921720/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-09T16:44:01.921720/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "BL8 1TF",  # wrong
            # split
            "BL9 8HB",
            "BL9 9PQ",
            "BL9 9JW",
            "BL9 8JJ",
            "BL8 2HH",
            "BL9 8JW",
        ]:
            return None

        return super().address_record_to_dict(record)
