from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BRC"
    addresses_name = "2024-05-02/2024-03-19T13:50:10.302143/Eros_SQL_Output003.csv"
    stations_name = "2024-05-02/2024-03-19T13:50:10.302143/Eros_SQL_Output003.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10022826533",  # THE BUNGALOW OAKWOOD PARK KENNELS PEACOCK LANE, WOKINGHAM
        ]:
            return None
        if record.housepostcode in [
            # split
            "SL5 8RY",
            "RG42 6BX",
        ]:
            return None
        return super().address_record_to_dict(record)
