from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RCC"
    addresses_name = (
        "2023-05-04/2023-04-05T14:43:08.187824/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-05T14:43:08.187824/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "TS10 4AJ",
            "TS6 0PA",
        ]:
            return None

        return super().address_record_to_dict(record)
