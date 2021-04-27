from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WAT"
    addresses_name = (
        "2021-04-19T09:17:40.372170/watford polling_station_export-2021-04-18.csv"
    )
    stations_name = (
        "2021-04-19T09:17:40.372170/watford polling_station_export-2021-04-18.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10023338176",  # 49 WILMINGTON CLOSE, WATFORD
        ]:
            return None

        if record.housepostcode in ["WD24 5DB", "WD17 4JT", "WD18 7BS"]:
            return None

        return super().address_record_to_dict(record)
