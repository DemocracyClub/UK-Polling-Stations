from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NNT"
    addresses_name = (
        "2024-02-15/2024-01-25T10:56:24.479815/Democracy_Club__15February2024.tsv"
    )
    stations_name = (
        "2024-02-15/2024-01-25T10:56:24.479815/Democracy_Club__15February2024.tsv"
    )
    elections = ["2024-02-15"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "NN8 1SH",
            "NN10 9JD",
            "NN10 9NJ",
            "NN8 4WG",
            "NN8 3JX",
            "NN29 7NL",
        ]:
            return None

        return super().address_record_to_dict(record)
