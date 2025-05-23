from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "LEE"
    addresses_name = "2025-05-29/2025-05-19T11:04:34.585409/Eros_SQL_Output001.csv"
    stations_name = "2025-05-29/2025-05-19T11:04:34.585409/Eros_SQL_Output001.csv"
    elections = ["2025-05-29"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "10033272374",  # 24A STEYNING AVENUE, PEACEHAVEN
                "200001466148",  # OLD WHEEL COTTAGE, EASTERN ROAD, WIVELSFIELD GREEN, HAYWARDS HEATH
                "100062487484",  # WOODS COTTAGE, EASTERN ROAD, WIVELSFIELD GREEN, HAYWARDS HEATH
            ]
        ):
            return None

        return super().address_record_to_dict(record)
