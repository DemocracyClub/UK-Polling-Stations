from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "COP"
    addresses_name = "2021-03-03T13:29:48.558281/polling_station_export-2021-03-02.csv"
    stations_name = "2021-03-03T13:29:48.558281/polling_station_export-2021-03-02.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode in [
            "CA25 5JE",
            "CA28 7QS",
            "CA28 6TU",
            "CA19 1UU",
            "CA25 5LN",
            "CA25 5LH",
            "CA22 2TD",
        ]:
            return None

        if uprn in ["10000890435"]:
            return None

        return super().address_record_to_dict(record)
