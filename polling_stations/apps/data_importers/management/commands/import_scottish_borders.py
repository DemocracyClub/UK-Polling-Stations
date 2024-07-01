from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SCB"
    addresses_name = "2024-07-04/2024-07-01T12:23:01.545943/SCB_PD_combined.csv"
    stations_name = "2024-07-04/2024-07-01T12:23:01.545943/SCB_PS_combined.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "TD6 0EB",
            "TD1 3NY",
            "EH45 9JJ",
        ]:
            return None
        if record.uprn in [
            "116074488",
            "116095151",
            "116054256",
        ]:
            return None
        return super().address_record_to_dict(record)
