from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "EDN"
    addresses_name = (
        "2022-05-05/2022-03-30T12:29:45.352395/polling_station_export-2022-03-24e.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-30T12:29:45.352395/polling_station_export-2022-03-24e.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "CA11 7UR",
            "CA11 8BX",
            "CA10 2DQ",
            "CA11 9HZ",
            "CA10 2BZ",
            "CA4 0HR",
            "CA9 3BU",
            "CA11 9RJ",
        ]:
            return None  # split

        uprn = record.uprn.lstrip("0")

        if uprn in [
            "10070544465",  # BRAMBLE HOUSE ACCESS ROAD TO MEADOW FLATT FROM THE B6277, ALSTON
        ]:
            return None

        return super().address_record_to_dict(record)
