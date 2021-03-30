from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "RUT"
    addresses_name = "2021-03-11T15:18:06.577876/polling_station_export-2021-03-11.csv"
    stations_name = "2021-03-11T15:18:06.577876/polling_station_export-2021-03-11.csv"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        if record.pollingstationname == "WHISSENDINE MEMORIAL HALL":
            record = record._replace(pollingstationpostcode="LE15 7ET")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.housepostcode in ["PE9 3SR"]:
            return None  # split

        return super().address_record_to_dict(record)
