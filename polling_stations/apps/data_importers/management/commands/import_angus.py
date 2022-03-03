from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ANS"
    addresses_name = (
        "2022-05-05/2022-02-11T11:29:59.770553/polling_station_export-2022-02-03.csv"
    )
    stations_name = (
        "2022-05-05/2022-02-11T11:29:59.770553/polling_station_export-2022-02-03.csv"
    )
    elections = ["2022-05-05"]


def address_record_to_dict(self, record):
    uprn = record.uprn.strip().lstrip("0")

    if record.housepostcode in ["DD9 7EZ", "DD8 2SF", "DD8 5PP", "DD8 2TJ"]:
        return None

    if uprn in ["117116533"]:
        return None

    return super().address_record_to_dict(record)
