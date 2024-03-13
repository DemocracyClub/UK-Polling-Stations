from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HRW"
    addresses_name = (
        "2024-05-02/2024-03-13T09:35:29.507827/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-13T09:35:29.507827/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
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
