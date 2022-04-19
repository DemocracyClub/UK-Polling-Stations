from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ELM"
    addresses_name = (
        "2022-05-05/2022-04-21T10:40:22.916723/polling_station_export-2022-04-21.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-21T10:40:22.916723/polling_station_export-2022-04-21.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "KT11 1DS",
            "KT8 9DU",
        ]:
            return None

        return super().address_record_to_dict(record)
