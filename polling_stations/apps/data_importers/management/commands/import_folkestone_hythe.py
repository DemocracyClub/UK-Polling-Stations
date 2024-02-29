from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SHE"
    addresses_name = "2024-05-02/2024-02-29T10:38:45.624345/Polling Districts.csv"
    stations_name = "2024-05-02/2024-02-29T10:38:45.624345/Polling Stations.csv"
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "TN29 9AU",
            "TN28 8PW",
            "CT20 3RE",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Amendment from council:
        # Old: Hawkinge Pavillion and Sports Ground, Pavillion Road, Hawkinge, Kent CT18 7AY
        # New: Hawkinge Pavilion and Sports Ground, Pavilion Road, Hawkinge, Kent, CT18 7UA
        if record.stationcode == "28":
            record = record._replace(
                xordinate="621844", yordinate="140755", postcode="CT18 7UA"
            )
        # 1st Lyminge Scout Hut, Woodland Road, Lyminge, Kent CT18 8EW
        if record.stationcode == "42":
            record = record._replace(xordinate="615894", yordinate="140864")

        return super().station_record_to_dict(record)
