from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRW"
    addresses_name = (
        "2023-05-04/2023-04-12T16:05:13.858320/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-12T16:05:13.858320/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # splits
            "CM14 5RT",
        ]:
            return None

        return super().address_record_to_dict(record)
