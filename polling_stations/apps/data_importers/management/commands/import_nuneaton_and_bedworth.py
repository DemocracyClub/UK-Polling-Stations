from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NUN"
    addresses_name = (
        "2025-05-01/2025-02-28T13:08:50.423474/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-28T13:08:50.423474/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100071496605",  # BRAMCOTE FIELDS FARM, LUTTERWORTH ROAD, BRAMCOTE, NUNEATON
            "100071235227",  # MEADOW FARM, LUTTERWORTH ROAD, BRAMCOTE, NUNEATON
        ]:
            return None

        if record.addressline6 in [
            # split
            "CV11 4NW",
            "CV11 6JF",
            "CV10 9QF",
            "CV11 6NL",
            "CV11 6JE",
            # suspect
            "CV12 9HJ",
            "CV10 0PL",
        ]:
            return None

        return rec
