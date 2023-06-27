from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SSO"
    addresses_name = "2023-07-20/2023-06-26T14:14:30/Eros_SQL_Output001_SSO.csv"
    stations_name = "2023-07-20/2023-06-26T14:14:30/Eros_SQL_Output001_SSO.csv"
    elections = ["2023-07-20"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "BA10 0BU",
            "TA10 0DL",
            "TA10 0HF",
            "TA3 6RP",
            "BA9 9NZ",
            "TA10 0QH",
            "TA10 0PJ",
        ]:
            return None

        return super().address_record_to_dict(record)
