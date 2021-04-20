from data_importers.ems_importers import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "POW"
    addresses_name = "2021-04-07T12:37:18.812269/polling_station_export-2021-04-07.csv"
    stations_name = "2021-04-07T12:37:18.812269/polling_station_export-2021-04-07.csv"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        if record.pollingstationnumber == "106":
            # Same station as station 146
            record = record._replace(
                pollingstationaddress_3="MACHYNLLETH",  # typo in original
                pollingstationpostcode="SY20 8ER",  # was SY20 8QR; copied from 146
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "SY18 6QT",
            "LD1 6TY",
            "LD1 6UT",
            "LD2 3UD",
            "HR3 5JY",
            "LD3 7HN",
            "LD3 9EF",
            "LD3 0HG",
            "SY16 3LS",
            "SY21 0NG",
            "SY21 0DT",
            "SY21 8QL",
            "SY22 6DE",
            "SY5 9BT",
            "SY21 9AN",
            "SY18 6JD",
            "SY16 3DR",
            "SY18 6LS",
            "SY18 6NR",
            "SY20 9NL",
            "SY10 0LH",
            "SY17 5SA",
            "SY17 5PA",
            "SY17 5NG",
            "SY20 8EX",
            "SY20 8DJ",
            "SY21 9AY",
            "SY21 9AP",
            "SY15 6LD",
            "SY22 5LX",
            "SY22 6JG",
            "SY22 6DG",
            "SY21 0HE",
            "SY16 3DW",
            "SY21 8TD",
            "SY21 7QU",
            "SY21 7NB",
            "SY21 9HZ",
        ]:
            return None  # split

        uprn = record.uprn.lstrip(" 0")

        if uprn in [
            "10011738931",  # in another area
        ]:
            return None

        return super().address_record_to_dict(record)
