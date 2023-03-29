from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROS"
    addresses_name = (
        "2023-05-04/2023-03-13T10:59:57.560334/Democracy_Club__04May2023 (1).tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-13T10:59:57.560334/Democracy_Club__04May2023 (1).tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "BB4 8TT",
            "OL13 0QR",
            # wrong
            "OL13 8PQ",
        ]:
            return None

        return super().address_record_to_dict(record)
