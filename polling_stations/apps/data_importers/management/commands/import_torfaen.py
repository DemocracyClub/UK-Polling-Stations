from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "TOF"
    addresses_name = (
        "2024-05-02/2024-03-08T13:10:09.629993/Export From Query for Caroline v4.csv"
    )
    stations_name = (
        "2024-05-02/2024-03-08T13:10:09.629993/Export From Query for Caroline v4.csv"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200002953910",  # PARK HOUSE FARM, GRAIG ROAD, UPPER CWMBRAN, CWMBRAN
        ]:
            return None

        if record.housepostcode.strip() in [
            # split
            "NP4 8LG",
            "NP4 7NW",
            "NP44 5AB",
            # suspect
            "NP4 8QW",
            "NP4 8QP",
            "NP4 6TX",
        ]:
            return None

        return super().address_record_to_dict(record)
