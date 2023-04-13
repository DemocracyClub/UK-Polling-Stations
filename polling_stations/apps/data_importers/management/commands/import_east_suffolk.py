from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ESK"
    addresses_name = "2023-05-04/2023-04-13T15:35:25.165461/East Suffolk Council - Democracy Club - Polling Districts May 2023.csv"
    stations_name = "2023-05-04/2023-04-13T15:35:25.165461/East Suffolk Council - Democracy Club - Polling Stations May 2023.csv"
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        if record.stationcode == "S110":
            # Dallinghoo Jubilee Hall
            record = record._replace(xordinate="", yordinate="")

        if record.stationcode == "S138":
            # Bruisyard Village Hall

            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in [
            "NR35 1BZ",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
