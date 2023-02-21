from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WND"
    addresses_name = (
        "2022-05-05/2022-02-10T14:02:53.128765/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-02-10T14:02:53.128765/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "SW17 7BB",
        ]:
            return None

        return super().address_record_to_dict(record)
