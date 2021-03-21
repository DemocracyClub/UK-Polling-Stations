from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GRA"
    addresses_name = "2021-03-04T15:08:48.032358/polling_station_export-2021-03-02.csv"
    stations_name = "2021-03-04T15:08:48.032358/polling_station_export-2021-03-02.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.housepostcode in ["DA11 0JT", "DA13 9EH", "ME3 7NB"]:
            return None

        if record.uprn.lstrip("0") in ["10012030386", "10012030387"]:
            return None

        return super().address_record_to_dict(record)
