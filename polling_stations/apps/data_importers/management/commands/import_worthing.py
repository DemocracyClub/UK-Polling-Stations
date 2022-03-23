from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOT"
    addresses_name = (
        "2022-05-05/2022-03-23T16:15:23.604159/Democracy_Club__05May2022WBC.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-23T16:15:23.604159/Democracy_Club__05May2022WBC.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"
