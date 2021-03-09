from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CHO"
    addresses_name = "2021-02-22T12:43:04.120748/polling_station_export-2021-02-17.csv"
    stations_name = "2021-02-22T12:43:04.120748/polling_station_export-2021-02-17.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.housepostcode in ["PR6 0BS", "PR6 0HT", "PR7 2QL"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if (
            record.pollingstationname == "ST JOHN THE DIVINE CHURCH HALL"
            and record.pollingstationaddress_2 == "COPPULL"
        ):
            # missing post code; new postcode from council
            # https://trello.com/c/zxf8MP5c/341-chorley
            record = record._replace(pollingstationpostcode="PR7 5AB")
        return super().station_record_to_dict(record)
