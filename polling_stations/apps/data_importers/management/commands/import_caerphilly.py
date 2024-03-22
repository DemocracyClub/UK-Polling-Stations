from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CAY"
    addresses_name = "2024-05-02/2024-03-22T14:36:48.765501/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-03-22T14:36:48.765501/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "43171669",  # THE LODGE, STABLES COMPOUND, WEST ROAD, PENALLTA INDUSTRIAL ESTATE, PENALLTA, HENGOED
        ]:
            return None
        if record.housepostcode in [
            "NP11 6JE",
            "CF83 8RL",
        ]:
            return None
        return super().address_record_to_dict(record)
