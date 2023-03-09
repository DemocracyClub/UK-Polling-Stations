from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HYN"
    addresses_name = (
        "2023-05-04/2023-03-09T16:17:00.789871/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-09T16:17:00.789871/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"


def address_record_to_dict(self, record):
    if record.addressline6 in [
        "BB5 5QA",  # split
    ]:
        return None

    return super().address_record_to_dict(record)
