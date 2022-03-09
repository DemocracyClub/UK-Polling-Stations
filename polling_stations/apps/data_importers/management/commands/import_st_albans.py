from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SAL"
    addresses_name = (
        "2022-05-05/2022-03-09T17:04:51.766114/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-09T17:04:51.766114/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "AL3 5PR",
            "AL4 0TP",
            "AL4 0TG",
            "AL3 5PD",
        ]:
            return None

        return super().address_record_to_dict(record)
