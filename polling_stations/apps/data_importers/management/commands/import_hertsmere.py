from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "HER"
    addresses_name = "2023-05-04/2023-04-28T15:50:50.877561/HertsmereBoroughCouncilEros_SQL_Output001.csv"
    stations_name = "2023-05-04/2023-04-28T15:50:50.877561/HertsmereBoroughCouncilEros_SQL_Output001.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "WD25 8BP",
        ]:
            return None
        return super().address_record_to_dict(record)
