from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CHT"
    addresses_name = (
        "2022-05-05/2022-02-25T12:48:35.558843/polling_station_export-2022-02-25.csv"
    )
    stations_name = (
        "2022-05-05/2022-02-25T12:48:35.558843/polling_station_export-2022-02-25.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):

        if record.housepostcode in [
            "GL50 2RF",
            "GL52 6RN",
            "GL52 2ES",
            "GL53 7AJ",
            "GL50 3RB",
            "GL53 0HL",
            "GL50 2DZ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.pollingstationnumber == "191":
            record = record._replace(pollingstationaddress_1="")
        return super().station_record_to_dict(record)
