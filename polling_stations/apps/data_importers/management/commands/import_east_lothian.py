from data_importers.ems_importers import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ELN"
    addresses_name = (
        "2021-03-22T10:01:23.121519/lothian ERO polling_station_export-2021-03-21.csv"
    )
    stations_name = (
        "2021-03-22T10:01:23.121519/lothian ERO polling_station_export-2021-03-21.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if (
            record.adminarea != "East Lothian"
            and record.town != "East Lothian"
            and record.town != "Musselburgh"
        ):
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if (
            record.adminarea != "East Lothian"
            and record.town != "East Lothian"
            and record.town != "Musselburgh"
        ):

            return None

        return super().station_record_to_dict(record)
