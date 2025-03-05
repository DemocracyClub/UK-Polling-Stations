from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ECA"
    addresses_name = "2025-05-01/2025-03-31T08:58:46.747046/Democracy Club - Polling Districts 2025.csv"
    stations_name = "2025-05-01/2025-03-31T08:58:46.747046/Democracy Club - Polling Stations 2025.csv"
    elections = ["2025-05-01"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if uprn in [
            "100090041333",  # 15 BLACK BANK ROAD, LITTLE DOWNHAM, ELY
            "100090041332",  # 17 BLACK BANK ROAD, LITTLE DOWNHAM, ELY
            "10095400067",  # 163 THE STREET, KIRTLING, NEWMARKET
        ]:
            return None

        return super().address_record_to_dict(record)
