from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EDE"
    addresses_name = (
        "2023-05-04/2023-03-15T16:02:12.044482/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-15T16:02:12.044482/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6.replace(" ", " ") in [
            # split
            "EX5 1LN",
            # wrong
            "EX8 2FQ",
        ]:
            return None

        return super().address_record_to_dict(record)
