from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DAL"
    addresses_name = (
        "2023-05-04/2023-03-30T16:58:57.312964/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-30T16:58:57.312964/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "DL1 2RG",
        ]:
            return None

        return super().address_record_to_dict(record)
