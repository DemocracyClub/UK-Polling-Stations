from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "CAB"
    addresses_name = "2026-05-07/2026-02-16T14:26:03.938575/Democracy Club - Idox_2026-02-16 14-12.csv"
    stations_name = "2026-05-07/2026-02-16T14:26:03.938575/Democracy Club - Idox_2026-02-16 14-12.csv"
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        # Adding missing UPRN from council for:
        # The Church of Jesus Christ of Latter-day Saints 670 Cherry Hinton Road Cambridge CB1 8ED
        if self.get_station_hash(record) in [
            "18-the-church-of-jesus-christ-of-latter-day-saints",
            "17-the-church-of-jesus-christ-of-latter-day-saints",
        ]:
            record = record._replace(
                pollingvenueuprn="200004216747",
                pollingvenueeasting="548424",
                pollingvenuenorthing="256186",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.uprn in [
            "10090966442",  # RIVERBOAT TUMBLING WATER G20635 RIVERSIDE, CAMBRIDGE
        ]:
            return None

        if record.postcode in [
            "CB3 0UW",  # split
        ]:
            return None
        return super().address_record_to_dict(record)
