from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SHE"
    addresses_name = "2025-05-01/2025-03-05T11:59:07.910870/Folkestone & Hythe - Polling district data.csv"
    stations_name = "2025-05-01/2025-03-05T11:59:07.910870/Folkestone & Hythe - Polling station data.csv"
    elections = ["2025-05-01"]
    csv_encoding = "utf-16le"
