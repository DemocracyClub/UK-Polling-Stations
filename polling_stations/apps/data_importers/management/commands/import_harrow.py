from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HRW"
    addresses_name = "2024-07-04/2024-06-19T11:48:48.902893/HRW_combined.tsv"
    stations_name = "2024-07-04/2024-06-19T11:48:48.902893/HRW_combined.tsv"
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
