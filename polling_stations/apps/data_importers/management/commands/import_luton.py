from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "LUT"
    addresses_name = "2021-03-17T12:07:50.769847/Luton DC - Polling Districts.csv"
    stations_name = "2021-03-17T12:07:50.769847/Luton DC - Polling Stations.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        self.postcode_field = "pcode"
        if record.pcode in ["LU3 1BU", "LU1 1BE"]:
            return None
        if uprn in ["10001037360", "200003278390"]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        self.postcode_field = "postcode"
        return super().station_record_to_dict(record)
