from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TEW"
    addresses_name = "2024-05-02/2024-04-02T08:48:18.759114/Democracy_Club__02May2024_Tewkesbury Borough.tsv"
    stations_name = "2024-05-02/2024-04-02T08:48:18.759114/Democracy_Club__02May2024_Tewkesbury Borough.tsv"
    elections = ["2024-05-02"]
    csv_delimiter = "\t"
