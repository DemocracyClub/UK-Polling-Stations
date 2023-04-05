from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NGM"
    addresses_name = (
        "2023-05-04/2023-04-05T16:34:11.754241/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-05T16:34:11.754241/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "NG7 1BZ",
        ]:
            return None

        return super().address_record_to_dict(record)
