from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SNO"
    addresses_name = "2021-03-04T15:54:30.296900/South Norfolk Democracy Club - Polling Districts - Election ID 7 County Council.csv"
    stations_name = "2021-03-04T15:54:30.296900/South Norfolk Democracy Club - Polling Stations - Election ID 7 County Council.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.postcode in ["IP21 4QR", "IP22 4JW", "NR18 0TR"]:
            return None

        return super().address_record_to_dict(record)
