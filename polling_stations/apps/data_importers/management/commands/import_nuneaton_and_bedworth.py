from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NUN"
    addresses_name = (
        "2024-05-02/2024-01-30T11:08:04.671172/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-01-30T11:08:04.671172/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline6 in [
            # split
            "CV11 6JF",
            "CV11 4NW",
            "CV10 9QF",
            "CV11 6JE",
            "CV11 6NL",
            # suspect
            "CV12 9HJ",
        ]:
            return None

        return rec
