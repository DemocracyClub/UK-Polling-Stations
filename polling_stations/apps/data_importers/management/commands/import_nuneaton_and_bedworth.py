from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NUN"
    addresses_name = (
        "2024-07-04/2024-06-01T22:49:27.542755/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-01T22:49:27.542755/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
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
