from data_importers.ems_importers import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SCB"
    addresses_name = "2021-03-25T12:10:21.663474/Democracy Club Polling Districts.csv"
    stations_name = "2021-03-25T12:10:21.663474/Democracy Club Polling Places.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.postcode in ["EH45 9JJ", "TD1 3NY", "TD12 4LG", "TD5 8PT"]:
            return None
        if record.uprn in [
            "116074488",
            "116090401",
            "116050796",
            "116060667",
            "116076251",
            "116062629",
        ]:
            return None
        return super().address_record_to_dict(record)
