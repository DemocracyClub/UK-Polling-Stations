from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "GOS"
    addresses_name = "2022-05-05/2022-03-07T15:47:28.644792/2022 Borough of Gosport - Democracy Club - Polling Districts v1 (07 03 2022).csv"
    stations_name = "2022-05-05/2022-03-07T15:47:28.644792/2022 Borough of Gosport - Democracy Club - Polling Stations v1 (07 03 2022).csv"
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.postcode in ["PO12 2EH"]:
            return None

        return super().address_record_to_dict(record)
