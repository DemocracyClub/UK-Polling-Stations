from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "THE"
    addresses_name = (
        "2023-05-04/2023-04-06T12:57:47.759538/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-06T12:57:47.759538/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "WD19 4LS",
        ]:
            return None

        return super().address_record_to_dict(record)
