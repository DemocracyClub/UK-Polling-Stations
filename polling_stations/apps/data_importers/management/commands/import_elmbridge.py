from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ELM"
    addresses_name = "2024-05-02/2024-02-20T17:29:24.243165/Eros_SQL_Output007.csv"
    stations_name = "2024-05-02/2024-02-20T17:29:24.243165/Eros_SQL_Output007.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100062356889",  # 1 ICKLINGHAM GATE, COBHAM
            "100061307354",  # BRACKENBURY, BYFLEET ROAD, COBHAM
            "100061326835",  # 133 BURWOOD ROAD, HERSHAM, WALTON-ON-THAMES
            "100061326833",  # 131 BURWOOD ROAD, HERSHAM, WALTON-ON-THAMES
        ]:
            return None

        return super().address_record_to_dict(record)
