from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ORK"
    addresses_name = "2022-05-05/2022-03-10T11:14:48.303621/polling_station_export-2022-03-07.csv 1.csv"
    stations_name = "2022-05-05/2022-03-10T11:14:48.303621/polling_station_export-2022-03-07.csv 1.csv"
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "KW15 1WU",
        ]:
            return None
        return super().address_record_to_dict(record)
