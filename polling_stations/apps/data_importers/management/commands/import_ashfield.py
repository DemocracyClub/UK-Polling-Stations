from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ASH"
    addresses_name = (
        "2024-07-04/2024-05-28T14:20:57.283721/Democracy_Club__04July2024 (1).tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-28T14:20:57.283721/Democracy_Club__04July2024 (1).tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "NG17 8JR",
            "NG17 8BE",
        ]:
            return None

        return super().address_record_to_dict(record)
