from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "BGE"
    addresses_name = "2026-05-07/2026-02-23T11:10:42.383762/BGE_combined.csv"
    stations_name = "2026-05-07/2026-02-23T11:10:42.383762/BGE_combined.csv"
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        # Removing bad coordinates for:
        # St John's Centre, SJAC, Minerva Street, Bridgend CF31 1TD
        if self.get_station_hash(record) == "86-st-johns-centre":
            record = record._replace(
                pollingvenueeasting="0",
                pollingvenuenorthing="0",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "CF31 2DH",
            "CF34 9SD",
            "CF32 8TY",
            "CF31 3HL",
            "CF36 3TB",
            "CF31 1NP",
            "CF34 0UF",
            "CF32 0NR",
            "CF35 6GD",
            "CF31 5FD",
            "CF35 6HZ",
        ]:
            return None

        return super().address_record_to_dict(record)
