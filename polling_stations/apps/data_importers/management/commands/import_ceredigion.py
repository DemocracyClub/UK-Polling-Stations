from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CGN"
    addresses_name = "2022-05-05/2022-04-14T13:37:04.763415/Democracy Club - Polling Districts CEREDIGION.csv"
    stations_name = "2022-05-05/2022-04-14T13:37:04.763415/Democracy Club - Polling Stations CEREDIGION.csv"
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.uprn.lstrip("0")

        if uprn in [
            "49062840",
            "49049138",
            "49069702",
            "49047840",
            "49040771",
            "49065819",
            "49069384",
            "49075931",
            "49037718",
            "49062368",
            "49061701",
            "49041491",
            "49040891",
            "49073822",
        ]:
            return None

        if record.postcode in ["SA43 1PT"]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # CANOLFAN CYMUNEDOL MYNACH COMMUNITY CENTRE
        if record.stationcode == "10-1026/1027":
            record = record._replace(postcode="")

        return super().station_record_to_dict(record)
