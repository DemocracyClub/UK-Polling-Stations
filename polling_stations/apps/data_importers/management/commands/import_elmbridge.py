from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "ELM"
    addresses_name = "2026-05-07/2026-03-05T18:03:47.545023/Democracy Club - Idox_2026-03-03 21-35.csv"
    stations_name = "2026-05-07/2026-03-05T18:03:47.545023/Democracy Club - Idox_2026-03-03 21-35.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100062356889",  # 1 ICKLINGHAM GATE, COBHAM
            "100061307354",  # BRACKENBURY, BYFLEET ROAD, COBHAM
            "100061326835",  # 133 BURWOOD ROAD, HERSHAM, WALTON-ON-THAMES
            "100061326833",  # 131 BURWOOD ROAD, HERSHAM, WALTON-ON-THAMES
            "100061307354",  # BRACKENBURY, BYFLEET ROAD, COBHAM
            "100061344692",  # 1 HIGH PINE CLOSE, WEYBRIDGE
        ]:
            return None

        return super().address_record_to_dict(record)
