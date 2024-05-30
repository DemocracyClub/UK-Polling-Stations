from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CMN"
    addresses_name = "2024-07-04/2024-06-05T13:06:51.093400/Eros_SQL_Output001.csv"
    stations_name = "2024-07-04/2024-06-05T13:06:51.093400/Eros_SQL_Output001.csv"
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        record = record._replace(pollingvenueuprn="")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.uprn in [
            "10004882480",  # PENYRHEOLWEN, TALLEY, LLANDEILO
            "10009546779",  # PENGOILAN, BETHLEHEM, LLANDEILO
            "10004853865",  # FLAT 1, 3 STATION ROAD, LLANELLI
            "10004848463",  # MERRY VALE, HALFPENNY FURZE, LAUGHARNE, CARMARTHEN
            "10009164875",  # COOMB LODGE, LLANYBRI, CARMARTHEN
        ]:
            return None

        if record.housepostcode in [
            # split
            "SA19 8TA",
            "SA15 5LP",
            "SA32 7AS",
            "SA16 0PP",
            "SA44 5YB",
            "SA31 3JJ",
            "SA19 7SG",
            "SA39 9EU",
            "SA19 7YE",
            "SA33 5DH",
            "SA15 1HP",
            "SA14 8TP",
            "SA14 8AY",
            "SA18 3DZ",
            "SA16 0LE",
            "SA18 3NB",
            "SA32 8BX",
            "SA32 7QJ",
            "SA14 8JA",
            "SA18 3TB",
            "SA17 5US",
            "SA34 0HX",
            "SA14 8BZ",
            "SA19 9AS",
            "SA39 9EJ",
            "SA19 8BR",
            "SA17 4NF",
            "SA20 0EY",
            # suspect
            "SA18 2ET",
            "SA15 1JE",
        ]:
            return None

        return super().address_record_to_dict(record)
