from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "LEE"
    addresses_name = "2024-07-04/2024-06-19T16:26:19.708577/LEE_combined.csv"
    stations_name = "2024-07-04/2024-06-19T16:26:19.708577/LEE_combined.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10033272374",  # 24A STEYNING AVENUE, PEACEHAVEN
            "200001466148",  # OLD WHEEL COTTAGE, EASTERN ROAD, WIVELSFIELD GREEN, HAYWARDS HEATH
            "100062487484",  # WOODS COTTAGE, EASTERN ROAD, WIVELSFIELD GREEN, HAYWARDS HEATH
        ]:
            return None

        return super().address_record_to_dict(record)
