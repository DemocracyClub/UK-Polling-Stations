from data_importers.ems_importers import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MLN"
    addresses_name = (
        "2021-03-22T10:03:09.388418/lothian ERO polling_station_export-2021-03-21.csv"
    )
    stations_name = (
        "2021-03-22T10:03:09.388418/lothian ERO polling_station_export-2021-03-21.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if (
            record.adminarea != "Midlothian"
            or (
                record.town == "Musselburgh"
                and record.pollingstationname != "Danderhall Leisure Centre"
            )
            or record.town == "Currie"
            or record.town == "Newbridge"
        ):
            return None

        if record.housepostcode in [
            "EH20 9AA",
            "EH20 9QA",
            "EH22 5TH",
            "EH23 4QA",
            "EH22 2EE",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if (
            record.adminarea != "Midlothian"
            or (
                record.town == "Musselburgh"
                and record.pollingstationname != "Danderhall Leisure Centre"
            )
            or record.town == "Currie"
            or record.town == "Newbridge"
        ):

            return None

        return super().station_record_to_dict(record)
