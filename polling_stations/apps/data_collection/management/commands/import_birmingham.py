from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E08000025"
    addresses_name = "local.2018-05-03/Version 3/polling_station_export-2018-04-17.csv"
    stations_name = "local.2018-05-03/Version 3/polling_station_export-2018-04-17.csv"
    elections = ["local.2018-05-03"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.housepostcode == "B71 1BX":
            return None

        if record.housepostcode == "B15 3QD":
            return None

        if record.housepostcode == "B31 2FL":
            return None

        if record.housepostcode == "B31 3JE":
            return None

        if record.housepostcode == "B32 2AQ":
            return None

        if record.housepostcode == "B6 6JU":
            return None

        if record.houseid == "48553":
            return None

        if record.housepostcode == "B9 4DS":
            return None

        if record.housepostcode == "B11 3EY":
            return None

        if record.housepostcode == "B15 3AY":
            return None

        return super().address_record_to_dict(record)
