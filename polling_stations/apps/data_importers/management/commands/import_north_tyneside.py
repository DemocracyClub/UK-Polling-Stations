from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NTY"
    addresses_name = (
        "2023-05-04/2023-03-10T12:13:25.758626/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-10T12:13:25.758626/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # SPLIT
            "NE12 8EE",
            # not sure
            "NE27 0XP",
            "NE13 6DX",
        ]:
            return None

        return super().address_record_to_dict(record)
