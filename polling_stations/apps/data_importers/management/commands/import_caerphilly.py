from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CAY"
    addresses_name = "2021-04-09T11:11:07.483794/polling_station_export-2021-04-08.csv"
    stations_name = "2021-04-09T11:11:07.483794/polling_station_export-2021-04-08.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.housepostcode in ["CF83 8RL", "NP11 6JE", "NP10 9GG"]:
            return None  # split

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.pollingstationnumber == "123":
            # Conflicting sources on postcode
            # Actual location: 318554.925,198088.857
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)
