from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "EDH"
    addresses_name = "2023-03-09/2023-02-24T13:04:29.352950/Eros_SQL_Output003.csv"
    stations_name = "2023-03-09/2023-02-24T13:04:29.352950/Eros_SQL_Output003.csv"
    elections = ["2023-03-09"]
