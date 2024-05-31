from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ERE"
    addresses_name = "2024-07-04/2024-05-31T16:32:38.579157/Eros_SQL_Output003.csv"
    stations_name = "2024-07-04/2024-05-31T16:32:38.579157/Eros_SQL_Output003.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        record.uprn.strip().lstrip("0")

        if record.uprn in [
            "100030142270",  # BARN END, CAT & FIDDLE LANE, WEST HALLAM, ILKESTON
        ]:
            return None

        return super().address_record_to_dict(record)
