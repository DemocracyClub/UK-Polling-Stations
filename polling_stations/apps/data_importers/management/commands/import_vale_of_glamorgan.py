from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "VGL"
    addresses_name = "2022-05-05/2022-03-11T14:01:39.044454/democracy club polling districts vale of glamorgan.csv"
    stations_name = "2022-05-05/2022-03-11T14:01:39.044454/democracy club polling stations vale of glamorgan.csv"
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.postcode in [
            "CF62 6BA",
        ]:
            return None
        return super().address_record_to_dict(record)
