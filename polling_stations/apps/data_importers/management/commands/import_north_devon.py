from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NDE"
    addresses_name = (
        "2023-05-04/2023-03-15T15:40:08.371986/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-15T15:40:08.371986/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "EX36 3DJ",
            "EX34 9QF",
            "EX32 8BS",
            "EX36 3BT",
            "EX32 0FE",
            "EX31 3XW",
            "EX39 4PF",
            "EX32 0PE",
            "EX33 2BW",
            "EX32 0AP",
            "EX33 2LN",
            "EX33 2NT",
            "EX33 1HW",
        ]:
            return None

        return super().address_record_to_dict(record)
