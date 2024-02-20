from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ERE"
    addresses_name = "2024-05-02/2024-02-20T16:22:55.849606/Eros_SQL_Output004.csv"
    stations_name = "2024-05-02/2024-02-20T16:22:55.849606/Eros_SQL_Output004.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        record.uprn.strip().lstrip("0")

        if record.uprn in [
            "100030142270",  # BARN END, CAT & FIDDLE LANE, WEST HALLAM, ILKESTON
        ]:
            return None

        return super().address_record_to_dict(record)
