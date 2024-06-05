from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MLN"
    addresses_name = "2024-07-04/2024-06-05T12:20:21.126261/Eros_SQL_Output005.csv"
    stations_name = "2024-07-04/2024-06-05T12:20:21.126261/Eros_SQL_Output005.csv"
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "120037867",  # DALHOUSIE MAINS DAIRY, DALKEITH
            "120035855",  # WEST LODGE, MELVILLE ESTATE, LASSWADE
        ]:
            return None
        if record.housepostcode in [
            # split
            "EH26 9AX",
            "EH22 2EE",
            "EH22 5TH",
            "EH23 4QA",
            "EH26 9AY",
            "EH20 9QA",
            "EH20 9AA",
            "EH22 5BG",
            "EH22 1SY",
        ]:
            return None
        return super().address_record_to_dict(record)
