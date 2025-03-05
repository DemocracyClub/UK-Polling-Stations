from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SHE"
    addresses_name = "2025-05-01/2025-03-05T11:59:07.910870/Folkestone & Hythe - Polling district data.csv"
    stations_name = "2025-05-01/2025-03-05T11:59:07.910870/Folkestone & Hythe - Polling station data.csv"
    elections = ["2025-05-01"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "50128053",  # APARTMENT 1, 4 DEARMAN CRESCENT, HYTHE
            "50128728",  # ASHBURY HOUSE 3 GREEN DRIVE, ETCHINGHILL
        ]:
            return None

        if record.postcode in [
            # split
            "TN28 8PW",
            "TN29 9AU",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Amendment from council:
        # Moves point closer to access road, corrects postcode:
        # Hawkinge Pavilion and Sports Ground, Pavilion Road, Hawkinge, Kent, CT18 7UA
        if record.stationcode == "28":
            record = record._replace(
                xordinate="621844",
                yordinate="140818",
                postcode="CT18 7UA",
            )
        return super().station_record_to_dict(record)
