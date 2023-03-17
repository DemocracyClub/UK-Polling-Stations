from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "LEE"
    addresses_name = "2023-05-04/2023-03-17T14:55:49.863600/Eros_SQL_Output001.csv"
    stations_name = "2023-05-04/2023-03-17T14:55:49.863600/Eros_SQL_Output001.csv"
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        if (
            record.pollingstationname
            == "SAINT PETER THE APOSTLE CHURCH HALL-THE CHAPEL ROOMS"
        ):
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "BN10 8UG",
        ]:
            return None

        return super().address_record_to_dict(record)
