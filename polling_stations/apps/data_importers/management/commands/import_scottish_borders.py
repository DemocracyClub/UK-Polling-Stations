from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SCB"
    addresses_name = "2022-05-05/2022-04-07T10:22:42.135500/Polling Districts.csv"
    stations_name = "2022-05-05/2022-04-07T10:22:42.135500/Polling Stations.csv"
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.postcode in [
            "TD1 3NY",
            "TD9 0SP",
        ]:
            return None
        if record.uprn in [
            "116074488",
            "116095151",
            "116054256",
        ]:
            return None
        return super().address_record_to_dict(record)
