from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ALL"
    addresses_name = "2022-05-05/2022-04-15T17:53:15.235889/Polling SDistricts.csv"
    stations_name = "2022-05-05/2022-04-15T17:53:15.235889/Polling Stations.csv"
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.postcode in ["CA15 7RL"]:
            return None  # split
        return super().address_record_to_dict(record)
