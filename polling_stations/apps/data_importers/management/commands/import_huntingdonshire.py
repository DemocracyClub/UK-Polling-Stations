from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HUN"
    addresses_name = "2024-07-04/2024-05-28T14:21:52.453156/HUN_combined.tsv"
    stations_name = "2024-07-04/2024-05-28T14:21:52.453156/HUN_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "PE28 2QG",
            "PE27 6DT",
            "PE19 1HW",
            # suspect
            "PE29 1NY",
            "PE28 4NS",
            "PE28 4EW",
        ]:
            return None

        return super().address_record_to_dict(record)
