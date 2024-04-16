from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NGM"
    addresses_name = (
        "2024-05-02/2024-04-05T10:54:15.030277/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-05T10:54:15.030277/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "NG5 2HL",  # split
        ]:
            return None
        return super().address_record_to_dict(record)
