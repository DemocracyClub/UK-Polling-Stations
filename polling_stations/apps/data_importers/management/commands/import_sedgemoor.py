from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SEG"
    addresses_name = "2021-03-04T13:46:19.027597/polling_station_export-2021-03-04.csv"
    stations_name = "2021-03-04T13:46:19.027597/polling_station_export-2021-03-04.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip()
        if record.housepostcode in [
            "TA6 5NL",
            "TA6 4HB",
            "TA5 2PF",
            "TA6 6RZ",
            "TA6 6QH",
            "TA6 6GD",
            "TA5 2BE",
            "BS24 0HT",
            "TA6 7AW",
            "TA5 2NH",
            "TA5 1JW",
        ]:
            return None

        if uprn == "10009328603":
            record = record._replace(housepostcode="TA5 1JG")

        return super().address_record_to_dict(record)
