from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRW"
    addresses_name = (
        "2024-05-02/2024-03-21T15:27:59.716517/Democracy_Club__02May2024 (22).tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-21T15:27:59.716517/Democracy_Club__02May2024 (22).tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "CM13 3HT",
            "CM15 0HZ",
            "CM14 5RT",
        ]:
            return None
        return super().address_record_to_dict(record)
