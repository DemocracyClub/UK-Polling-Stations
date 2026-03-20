from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "FAL"
    addresses_name = "2026-05-07/2026-03-20T15:50:53.914809/Democracy Club Falkirk- Idox_2026-03-20 15-43.csv"
    stations_name = "2026-05-07/2026-03-20T15:50:53.914809/Democracy Club Falkirk- Idox_2026-03-20 15-43.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "136023196",  # 117 CARRONSHORE ROAD, CARRON, FALKIRK
            "136023197",  # 119 CARRONSHORE ROAD, CARRON, FALKIRK
        ]:
            return None

        if record.postcode in [
            # splits
            "FK2 7FG",
        ]:
            return

        return super().address_record_to_dict(record)
