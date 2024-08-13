from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "NOW"
    addresses_name = "2024-07-04/2024-06-12T10:48:23.075732/NOW_districts_combined.csv"
    stations_name = "2024-07-04/2024-06-12T10:48:23.075732/Democracy Club Polling Stations Norwich 20240604.csv"
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # Removing the following stations because they are outside of the council boundaries and have no addresses assigned:
        if record.stationcode in [
            "NS42",
            "NS41",
        ]:
            return None

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "10024023874",  # LIVING ACCOMMODATION THE MARSH HARRIER IPSWICH ROAD, NORWICH
                "200004349456",  # 14A IPSWICH ROAD, NORWICH
            ]
        ):
            return None

        return super().address_record_to_dict(record)
