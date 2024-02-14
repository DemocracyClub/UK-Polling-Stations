from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "GOS"
    addresses_name = "2024-05-02/2024-02-14T15:34:50.440698/2024 LGE & PCC - Democracy Club - Polling Districts.csv"
    stations_name = "2024-05-02/2024-02-14T15:34:50.440698/2024 LGE & PCC - Democracy Club - Polling Stations.csv"
    elections = ["2024-05-02"]

    def station_record_to_dict(self, record):
        # St. Marys Church Parish Centre, Green Road, Gosport, Hampshire
        if record.stationcode == "3AL3" or record.stationcode == "4AN1":
            record = record._replace(xordinate="460159", yordinate="98802")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in [
            # suspect
            "PO12 1SE",
            "PO12 4AW",
            "PO12 4QE",
            "PO12 4JP",
        ]:
            return None

        return super().address_record_to_dict(record)
