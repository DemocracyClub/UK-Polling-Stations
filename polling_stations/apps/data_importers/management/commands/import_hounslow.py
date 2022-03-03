from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HNS"
    addresses_name = (
        "2022-05-05/2022-02-21T16:49:40.581288/Democracy_Club__05May2022.CSV"
    )
    stations_name = (
        "2022-05-05/2022-02-21T16:49:40.581288/Democracy_Club__05May2022.CSV"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "TW8 0QS",
            "W4 1TF",
            "W4 4EU",
            "TW4 6DH",
            "TW13 6AB",
            "TW3 3DW",
            "TW4 5HS",
        ]:
            return None

        return super().address_record_to_dict(record)
