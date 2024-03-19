from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NED"
    addresses_name = (
        "2024-05-02/2024-03-19T16:44:48.987027/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-19T16:44:48.987027/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"
