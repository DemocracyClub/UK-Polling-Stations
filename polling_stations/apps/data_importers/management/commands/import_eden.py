from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "EDN"
    addresses_name = "2021-03-08T13:56:09.776816/polling_station_export-2021-03-08.csv"
    stations_name = "2021-03-08T13:56:09.776816/polling_station_export-2021-03-08.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "CA11 9HZ",
            "CA11 7UR",
            "CA10 2DQ",
            "CA10 2BZ",
            "CA11 8BX",
        ]:
            return None  # split

        if record.housepostcode in [
            "CA9 3DD",  # surrounded by properties for another polling stations
        ]:
            return None

        rec = super().address_record_to_dict(record)

        if record.houseid == "9143":
            rec["postcode"] = "CA110TY"  # "O" -> "0"

        return rec
