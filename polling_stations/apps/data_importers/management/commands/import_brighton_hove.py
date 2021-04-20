from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BNH"
    addresses_name = (
        "2021-03-31T10:12:51.372204/Brighton and Hove Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-03-31T10:12:51.372204/Brighton and Hove Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline6 in ["BN2 4RF", "BN1 7ET", "BN1 8NF", "BN1 3AE"]:
            return None  # split

        return rec
