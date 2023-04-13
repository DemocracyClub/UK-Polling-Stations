from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CLD"
    addresses_name = (
        "2023-05-04/2023-04-13T15:17:42.827927/Calderdale Polling Districts 2023.csv"
    )
    stations_name = (
        "2023-05-04/2023-04-13T15:17:42.827927/Calderdale Polling Stations 2023.csv"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "OL14 6RS",
            "HX3 5JF",
        ]:
            return None

        return super().address_record_to_dict(record)
