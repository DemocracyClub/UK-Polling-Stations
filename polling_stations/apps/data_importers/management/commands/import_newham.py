from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWM"
    addresses_name = "2024-07-04/2024-06-20T13:52:40.152721/ForestGateNorthandMaryland_Democracy_Club__04July2024.tsv"
    stations_name = "2024-07-04/2024-06-20T13:52:40.152721/ForestGateNorthandMaryland_Democracy_Club__04July2024.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"
