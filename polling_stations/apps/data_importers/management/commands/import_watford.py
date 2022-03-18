from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WAT"
    addresses_name = "2022-05-05/2022-03-28T12:27:39.290212/Eros_SQL_Output028.csv"
    stations_name = "2022-05-05/2022-03-28T12:27:39.290212/Eros_SQL_Output028.csv"
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        # All UPRNs have a leading "'"
        uprn = record.uprn.replace("'", "").strip()
        record = record._replace(uprn=uprn)

        if record.housepostcode in [
            "WD25 9AS",
            "WD25 7DA",
            "WD18 7BS",
        ]:
            return None
        return super().address_record_to_dict(record)
