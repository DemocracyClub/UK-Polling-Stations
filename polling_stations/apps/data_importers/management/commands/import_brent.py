from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BEN"
    addresses_name = "2021-03-30T11:24:08.732705/Brent DC -polling districts.csv"
    stations_name = "2021-03-30T11:24:08.732705/Brent DC -polling stations (2).csv"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        if record.stationcode == "CDU4_1":
            record = record._replace(yordinate="184797")
            record = record._replace(xordinate="521445")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if uprn in [
            "202228638",
            "202038378",
            "202228580",
            "202053053",
            "202053054",
        ]:
            return None

        return super().address_record_to_dict(record)
