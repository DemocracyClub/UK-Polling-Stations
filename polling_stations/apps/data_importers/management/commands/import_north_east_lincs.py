from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NEL"
    addresses_name = "2023-05-04/2023-03-17T16:58:51.018219/Eros_SQL_Output001.csv"
    stations_name = "2023-05-04/2023-03-17T16:58:51.018219/Eros_SQL_Output001.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10090078903",  # FLAT, 247 GRIMSBY ROAD, CLEETHORPES
            "10090086605",  # THE ROOST, DIANA PRINCESS OF WALES HOSPITAL, SCARTHO ROAD, GRIMSBY
        ]:
            return None

        return super().address_record_to_dict(record)
