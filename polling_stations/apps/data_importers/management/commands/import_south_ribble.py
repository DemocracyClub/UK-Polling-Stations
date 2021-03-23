from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SRI"
    addresses_name = (
        "2021-03-09T23:18:28.806724/South Ribble polling_station_export-2021-03-09.csv"
    )
    stations_name = (
        "2021-03-09T23:18:28.806724/South Ribble polling_station_export-2021-03-09.csv"
    )
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.housepostcode in ["PR5 5AU", "PR5 4TB"]:
            return None
        return super().address_record_to_dict(record)
