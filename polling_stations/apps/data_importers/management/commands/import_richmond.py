from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RIC"
    addresses_name = (
        "2022-05-05/2022-02-22T10:39:44.138903/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-02-22T10:39:44.138903/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "TW12 2SB",
            "TW2 5NJ",
        ]:
            return None

        return super().address_record_to_dict(record)
