from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHO"
    addresses_name = (
        "2025-05-01/2025-02-27T14:52:21.008684/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-27T14:52:21.008684/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "PE12 6HJ",
            "PE11 1XP",
            "PE6 0LR",
            "PE12 9QJ",
        ]:
            return None

        return super().address_record_to_dict(record)
