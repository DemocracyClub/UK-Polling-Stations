from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CMN"
    addresses_name = "2024-05-02/2024-02-22T09:38:19.926469/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-02-22T09:38:19.926469/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"

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
            "SA18 3DZ",
            "SA44 5YB",
            "SA33 5DH",
            "SA39 9EU",
            "SA16 0PP",
            "SA14 8TP",
            "SA34 0HX",
            "SA15 1HP",
            "SA39 9EJ",
            "SA15 5LP",
            "SA16 0LE",
            "SA32 7AS",
            "SA19 7YE",
            "SA19 8TA",
            "SA32 8BX",
            "SA34 0XA",
            "SA14 8JA",
            "SA14 8AY",
            "SA31 3JJ",
            "SA32 7QJ",
            "SA19 8BR",
            "SA14 8BZ",
            "SA20 0EY",
            "SA18 3TB",
            "SA17 5US",
            "SA19 7SG",
            "SA18 3NB",
            "SA17 4NF",
            "SA19 9AS",
            # suspect
            "SA18 2ET",
            "SA15 1JE",
        ]:
            return None

        return super().address_record_to_dict(record)
