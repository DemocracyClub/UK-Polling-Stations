from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MSS"
    addresses_name = (
        "2023-05-04/2023-03-03T13:09:09.891542/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-03T13:09:09.891542/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.post_code in ["RH17 7DY", "BN6 9NA", "RH16 2QB"]:
            return None

        return super().address_record_to_dict(record)
