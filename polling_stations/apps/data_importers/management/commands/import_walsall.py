from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WLL"
    addresses_name = "2023-05-04/2023-03-29T14:11:04.952178/Eros_SQL_Output001.csv"
    stations_name = "2023-05-04/2023-03-29T14:11:04.952178/Eros_SQL_Output001.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100071072854",  # 59 NEW STREET, SHELFIELD, WALSALL
            "100071072810",  # 9A NEW STREET, SHELFIELD, WALSALL
            "10090903310",  # FLAT 1 73 STAFFORD STREET, WILLENHALL
            "200002877500",  # 43A HIGH STREET, BROWNHILLS, WALSALL
        ]:
            return None

        if record.housepostcode in [
            # split
            "WS3 1FJ",
            "WS1 3LD",
            "WV12 4BZ",
            "WS3 2DX",
            # look wrong
            "WS10 7TG",
            "WS2 0HS",
            "WS3 4LX",
            "WS3 4NX",
        ]:
            return None

        return super().address_record_to_dict(record)
