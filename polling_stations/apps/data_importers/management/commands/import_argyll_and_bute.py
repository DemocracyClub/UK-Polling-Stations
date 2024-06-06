from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "AGB"
    addresses_name = "2024-07-04/2024-06-06T10:18:55.085692/Eros_SQL_Output003 (3).csv"
    stations_name = "2024-07-04/2024-06-06T10:18:55.085692/Eros_SQL_Output003 (3).csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "125056372",  # CRAIGALLAN, ASCOG, ISLE OF BUTE
            "125084307",  # ROWAN LEA, CRAIGNURE, ISLE OF MULL
        ]:
            return None

        if record.housepostcode in [
            # split
            "PA28 6PX",
            "PA37 1PE",
            "PA23 7AL",
            "PA33 1BX",
            "G84 7BF",
        ]:
            return None
        return super().address_record_to_dict(record)
