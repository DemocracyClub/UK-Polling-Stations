from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SCE"
    addresses_name = "2021-11-10T10:12:49.277177/polling_station_export-2021-11-10.csv"
    stations_name = "2021-11-10T10:12:49.277177/polling_station_export-2021-11-10.csv"
    elections = ["2021-11-25"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "YO21 1SU",
            "YO12 5DB",
            "YO14 9EW",
            "YO21 3JU",
            "YO21 3FP",
            "YO11 3PQ",
        ]:
            return None

        if record.uprn == "10023875937":  # 3 POSTGATE WAY, UGTHORPE, WHITBY
            return None

        return super().address_record_to_dict(record)
