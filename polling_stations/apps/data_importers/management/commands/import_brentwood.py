from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRW"
    addresses_name = (
        "2024-07-04/2024-06-27T13:18:28.950349/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-27T13:18:28.950349/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
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
