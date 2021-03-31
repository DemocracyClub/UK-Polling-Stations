from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WNM"
    addresses_name = "2021-03-25T12:59:22.400019/polling_station_export-2021-03-24.csv"
    stations_name = "2021-03-25T12:59:22.400019/polling_station_export-2021-03-24.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100081050796",  # PENNYFIELD, SWITCHBACK ROAD NORTH, MAIDENHEAD
        ]:
            return None

        if record.housepostcode in ["SL6 2QS", "SL6 3DU", "SL4 3FG", "SL5 9RP"]:
            return None

        return super().address_record_to_dict(record)
