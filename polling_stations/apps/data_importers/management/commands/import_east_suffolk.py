from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ESK"
    addresses_name = "2026-05-07/2026-03-04T14:10:09.553919/East Suffolk Council - Polling Districts 07.05.26 - Unopened.csv"
    stations_name = "2026-05-07/2026-03-04T14:10:09.553919/East Suffolk Council - Polling Stations 07.05.26 - Unopened.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100091154936",  # 6 THE PIGHTLE, NORTH COVE, BECCLES
            "100091487163",  # ISLAND COTTAGE, THE STREET, HACHESTON, WOODBRIDGE
            "100091638545",  # HEATH COTTAGE, FOXHALL, IPSWICH
        ]:
            return None

        if record.postcode in [
            # splits
            "NR35 1BZ",
            # suspect
            "NR34 8ET",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Location correction for: Castle Community Rooms, Church Street, Framlingham, Woodbridge, IP13 9BQ
        if record.stationcode == "S123":
            record = record._replace(xordinate="628574", yordinate="263554")

        return super().station_record_to_dict(record)
