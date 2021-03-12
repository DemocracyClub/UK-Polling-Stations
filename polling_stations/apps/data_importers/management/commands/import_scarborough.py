from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SCE"
    addresses_name = "2021-03-19T11:28:59.858425/polling_station_export-2021-03-19.csv"
    stations_name = "2021-03-19T11:28:59.858425/polling_station_export-2021-03-19.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.housepostcode in ["YO11 3NH", "YO21 1SU", "YO21 3JU"]:
            return None

        return super().address_record_to_dict(record)
