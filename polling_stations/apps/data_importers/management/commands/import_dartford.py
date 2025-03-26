from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "DAR"
    addresses_name = "2025-05-01/2025-03-26T12:58:37.459986/Eros_SQL_Output001.csv"
    stations_name = "2025-05-01/2025-03-26T12:58:37.459986/Eros_SQL_Output001.csv"
    elections = ["2025-05-01"]

    def station_record_to_dict(self, record):
        # Removing suspect station:
        if self.get_station_hash(record) == "99-mobile-unit-or-polling-station-gre4":
            return None

        # Adding missing coords to 2nd station at the same venue as a station with coords
        if self.get_station_hash(record) == "24-long-valley-hall-lns2":
            record = record._replace(
                pollingvenueeasting="559819",
                pollingvenuenorthing="169259",
                pollingvenueuprn="200000538035",
            )

        return super().station_record_to_dict(record)
