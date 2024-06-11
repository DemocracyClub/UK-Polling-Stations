from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HRW"
    addresses_name = (
        "2024-07-04/2024-06-11T08:45:16.958438/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-11T08:45:16.958438/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "HA1 2LH",
            "HA5 3HF",
            # suspect
            "HA1 1HQ",
            "HA1 4GT",
        ]:
            return None
        return super().address_record_to_dict(record)
