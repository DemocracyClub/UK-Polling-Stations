from data_importers.ems_importers import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):

    council_id = "VGL"
    addresses_name = "2021-04-13T09:25:56.187046/Polling Districts.csv"
    stations_name = "2021-04-13T09:25:56.187046/Polling Stations.csv"

    elections = ["2021-05-06"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.postcode in ["CF62 6BA", "CF64 4TA", "CF71 7QR"]:
            return None
        return super().address_record_to_dict(record)
