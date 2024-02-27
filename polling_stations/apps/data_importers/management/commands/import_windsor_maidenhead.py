from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "WNM"
    addresses_name = (
        "2024-05-02/2024-02-27T18:19:44.691508/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2024-05-02/2024-02-27T18:19:44.691508/Democracy Club - Polling Stations.csv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        # Polling station A Mobile Unit at Waitrose Carpark
        if record.stationcode == "62WSC3":
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10012304920",  # LONG WALK GATE LODGE, FROGMORE, WINDSOR
        ]:
            return None

        return super().address_record_to_dict(record)
