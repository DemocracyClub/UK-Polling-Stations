from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRF"
    addresses_name = (
        "2022-05-05/2022-03-03T10:11:12.032905/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-03T10:11:12.032905/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):

        if record.addressline6 in ["CF24 2DG", "CF3 4LL", "CF14 9UA"]:
            return None

        return super().address_record_to_dict(record)
