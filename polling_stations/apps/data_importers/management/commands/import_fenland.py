from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "FEN"
    addresses_name = "2025-05-01/2025-03-11T14:58:14.457984/Democracy Club FDC Polling Districts for May 2025.csv"
    stations_name = "2025-05-01/2025-03-11T14:58:14.457984/Democracy Club FDC Polling Stations for May 2025.csv"
    elections = ["2025-05-01"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.postcode in [
            "PE14 0LF",  # split
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Removing suspect coordinates pending council confirmation for the following station:
        # Chatteris Library 2 Furrowfields Road Chatteris Cambridgeshire, PE16 6DY
        if record.stationcode == "1":
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)
