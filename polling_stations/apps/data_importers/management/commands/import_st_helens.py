from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHN"
    addresses_name = "2025-04-03/2025-03-20T09:55:21.248536/Democracy_Club__03April2025 - Sutton South East By Election.tsv"
    stations_name = "2025-04-03/2025-03-20T09:55:21.248536/Democracy_Club__03April2025 - Sutton South East By Election.tsv"
    elections = ["2025-04-03"]
    csv_delimiter = "\t"
