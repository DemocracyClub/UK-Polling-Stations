from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ANS"
    addresses_name = (
        "2021-03-04T10:52:18.139732/Angus polling_station_export-2021-03-04.csv"
    )
    stations_name = (
        "2021-03-04T10:52:18.139732/Angus polling_station_export-2021-03-04.csv"
    )
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode in [
            "DD9 7EZ",
            "DD8 2SF",
            "DD8 4QB",
            "DD8 5PP",
            "DD8 2TJ",
            "DD11 3ET",
            "DD8 4QH",
        ]:
            return None

        if uprn in ["117078908", "117116533"]:
            return None

        return super().address_record_to_dict(record)
