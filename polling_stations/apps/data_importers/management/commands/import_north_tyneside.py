from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NTY"
    addresses_name = (
        "2022-05-05/2022-03-11T10:10:41.451729/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-11T10:10:41.451729/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in ["NE12 8EE", "NE27 0XP"]:
            return None

        return super().address_record_to_dict(record)
