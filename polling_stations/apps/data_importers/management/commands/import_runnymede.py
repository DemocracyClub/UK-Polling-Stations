from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUN"
    addresses_name = (
        "2022-05-05/2022-03-03T14:49:14.647146/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-03T14:49:14.647146/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in ["KT16 8QD", "KT16 8AG"]:
            return None

        return super().address_record_to_dict(record)
