from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BGW"
    addresses_name = "2024-05-02/2024-03-20T09:59:04.174956/Eros_SQL_Output008.csv"
    stations_name = "2024-05-02/2024-03-20T09:59:04.174956/Eros_SQL_Output008.csv"
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100100460975",  # 27A QUEEN STREET, NANTYGLO
            "100100460974",  # 27B QUEEN STREET, NANTYGLO
            "10014116610",  # 1 MOUNTAIN AIR, EBBW VALE
            "10014116959",  # 8 RESERVOIR ROAD, BEAUFORT, EBBW VALE
        ]:
            return None

        if record.housepostcode in [
            "NP23 5DH",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
