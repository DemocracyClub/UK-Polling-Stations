from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROT"
    addresses_name = (
        "2022-05-05/2022-03-14T15:37:24.025153/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-14T15:37:24.025153/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "S64 8PG",
            "S81 8BA",
        ]:
            return None

        return super().address_record_to_dict(record)
