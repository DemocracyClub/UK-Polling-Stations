from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "POW"
    addresses_name = (
        "2022-05-05/2022-04-04T12:17:28.212236/polling_station_export-2022-03-30.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-04T12:17:28.212236/polling_station_export-2022-03-30.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "SY5 9BT",
            "LD3 0HG",
            "SY20 8DJ",
            "LD3 9EF",
            "SY21 9AN",
            "HR3 5JY",
            "SY16 3DR",
            "SY17 5PA",
            "SY15 6LD",
            "LD1 6TY",
            "SY16 1HG",
            "SY10 0LH",
            "LD3 7HN",
            "SY22 6DE",
            "SY17 5SA",
            "SY22 5LX",
            "SY17 5NG",
            "SY18 6QT",
            "SY18 6LS",
            "LD1 6UT",
            "SY16 3LS",
            "SY21 0HE",
            "SY18 6LT",
            "SY18 6JD",
            "SY16 3DW",
            "SY18 6NR",
            "SY21 9AY",
            "SY21 9HZ",
            "SY21 0NG",
            "SY20 8EX",
            "SY21 7QU",
            "SY21 0DT",
            "SY21 8TD",
            "SY22 6JG",
            "LD2 3UD",
            "SY21 9AP",
        ]:
            return None  # split

        uprn = record.uprn.lstrip(" 0")

        if uprn in ["10011795190"]:
            return None

        return super().address_record_to_dict(record)
