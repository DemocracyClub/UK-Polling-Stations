from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NEL"
    addresses_name = (
        "2022-05-05/2022-03-24T10:29:54.923749/polling_station_export-2022-03-24.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-24T10:29:54.923749/polling_station_export-2022-03-24.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in []:
            return None

        if record.housepostcode in [
            "DN33 2AD",
        ]:
            return None

        return super().address_record_to_dict(record)
