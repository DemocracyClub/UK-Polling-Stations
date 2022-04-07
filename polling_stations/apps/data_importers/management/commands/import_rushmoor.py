from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUH"
    addresses_name = (
        "2022-05-05/2022-04-07T15:35:53.022248/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-07T15:35:53.022248/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in ["GU14 8UL"]:
            return None

        return super().address_record_to_dict(record)
