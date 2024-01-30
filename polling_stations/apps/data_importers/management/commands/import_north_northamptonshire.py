from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NNT"
    addresses_name = "2024-02-15/2024-01-30T16:43:45.816756/Democracy_Club__15February2024_version2.tsv"
    stations_name = "2024-02-15/2024-01-30T16:43:45.816756/Democracy_Club__15February2024_version2.tsv"
    elections = ["2024-02-15"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "NN10 9NJ",
            "NN8 4WG",
            "NN10 9JD",
            "NN8 1SH",
            "NN8 3JX",
            "NN29 7NL",
        ]:
            return None

        return super().address_record_to_dict(record)
