from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DEN"
    addresses_name = (
        "2021-03-24T11:39:12.706041/Denbighshire Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-03-24T11:39:12.706041/Denbighshire Democracy_Club__06May2021.tsv"
    )
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.addressline6 in ["LL18 4DP"]:
            return None  # split

        return super().address_record_to_dict(record)
