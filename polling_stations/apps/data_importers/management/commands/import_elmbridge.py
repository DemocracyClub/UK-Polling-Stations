from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ELM"
    addresses_name = "2023-05-04/2023-03-09T12:52:17.627189/Elmbridge_Democracy Club data_Eros_SQL_Output004.csv"
    stations_name = "2023-05-04/2023-03-09T12:52:17.627189/Elmbridge_Democracy Club data_Eros_SQL_Output004.csv"
    elections = ["2023-05-04"]
