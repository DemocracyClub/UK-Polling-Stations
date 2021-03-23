from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "LIC"
    addresses_name = "2021-03-10T14:31:40.987791/polling_station_export-2021-03-10.csv"
    stations_name = "2021-03-10T14:31:40.987791/polling_station_export-2021-03-10.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "LN2 4DY",
            "LN2 4NA",
            "LN1 3EJ",
            "LN1 1XE",
            "LN2 5HZ",
            "LN2 5EJ",
            "LN2 5LY",
            "LN2 4PA",
            "LN1 1AW",
            "LN1 1BU",
            "LN1 1DR",
            "LN6 8AZ",
            "LN6 7HR",
            "LN5 8RT",
            "LN6 8DB",
            "LN6 0HX",
            "LN6 0LU",
        ]:
            return None

        return super().address_record_to_dict(record)
