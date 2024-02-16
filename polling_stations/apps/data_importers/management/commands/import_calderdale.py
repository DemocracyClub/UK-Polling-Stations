from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CLD"
    addresses_name = "2024-05-02/2024-02-16T15:25:54.920405/2024 02 16 Democracy Club Polling Districts export.csv"
    stations_name = "2024-05-02/2024-02-16T15:25:54.920405/2024 02 16 Democracy Club Polling Stations export.csv"
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        # LEE MOUNT BAPTIST CHURCH, MELBOURNE STREET, LEE MOUNT, HALIFAX, WEST YORKSHIRE HX3 5BQ
        if record.stationcode == "60JB":
            record = record._replace(xordinate="408412")
            record = record._replace(yordinate="426427")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.uprn in [
            "10093206213",  # 1 PARKIN LANE, TODMORDEN
            "10093208972",  # GREAT LEAR INGS BARN, HEPTONSTALL, HEBDEN BRIDGE
        ]:
            return None

        if record.postcode in [
            "HX2 0UW",  # suspect
        ]:
            return None

        return super().address_record_to_dict(record)
