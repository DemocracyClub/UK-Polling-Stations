from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ISL"
    addresses_name = "2024-08-15/2024-08-12T11:26:42.456008/Democracy_Club__15August2024HillriseWardIslington.tsv"
    stations_name = "2024-08-15/2024-08-12T11:26:42.456008/Democracy_Club__15August2024HillriseWardIslington.tsv"
    elections = ["2024-08-15"]
    csv_delimiter = "\t"
