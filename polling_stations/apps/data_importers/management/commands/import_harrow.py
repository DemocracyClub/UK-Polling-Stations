from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HRW"
    addresses_name = (
        "2022-05-05/2022-03-28T16:53:48.820120/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-28T16:53:48.820120/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6.strip() in ["HA5 3HF"]:
            return None  # split

        return super().address_record_to_dict(record)
