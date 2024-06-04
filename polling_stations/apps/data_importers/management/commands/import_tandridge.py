from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "TAN"
    addresses_name = "2024-07-04/2024-06-04T17:04:40.456886/Eros_SQL_Output006.csv"
    stations_name = "2024-07-04/2024-06-04T17:04:40.456886/Eros_SQL_Output006.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200000141065",  # OLD MOAT BARN, ARDENRUN, LINGFIELD
            "200000140050",  # SURREY BEECHES, WESTERHAM ROAD, WESTERHAM
            "200000140051",  # SURREY BEECHES WEST, WESTERHAM ROAD, WESTERHAM
            "100061586276",  # CLOVERLAY, ROCKFIELD ROAD, OXTED
        ]:
            return None

        if record.housepostcode in [
            "CR6 9LB",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
