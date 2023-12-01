from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NKE"
    addresses_name = (
        "2023-12-14/2023-11-29T10:46:46.876779/NKDC Polling Stn Finder.tsv"
    )
    stations_name = (
        "2023-12-14/2023-11-29T10:46:46.876779/NKDC Polling Stn Finder.tsv"
    )
    elections = ["2023-12-14"]
    csv_delimiter = "\t"
