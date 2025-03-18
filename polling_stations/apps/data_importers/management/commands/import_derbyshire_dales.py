from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "DEB"
    addresses_name = "2025-05-01/2025-03-03T17:09:19.316607/Democracy Club Polling Districts County Council Election 1 May 2025.csv"
    stations_name = "2025-05-01/2025-03-03T17:09:19.316607/Democracy Club Polling Stations County Council Election 1 May 2025.csv"
    elections = ["2025-05-01"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        # Removes polling stations name duplication in addresses
        record = record._replace(add1="")

        # Coord corrections from council for:
        # ASHBOURNE LIBRARY COMPTON ASHBOURNE DERBYSHIRE
        if record.stationcode == "2":
            record = record._replace(xordinate="418090", yordinate="346551")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10070103452",  # 109 WELLINGTON STREET, MATLOCK
            "10010344035",  # 9 OLD METHODIST CHURCH, BANK ROAD, MATLOCK
        ]:
            return None

        if record.postcode in [
            "DE6 2AR",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
