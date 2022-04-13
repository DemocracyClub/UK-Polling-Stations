from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "RYE"
    addresses_name = (
        "2022-05-05/2022-04-13T15:03:49.381329/polling_station_export-2022-03-03.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-13T15:03:49.381329/polling_station_export-2022-03-03.csv"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):

        # Swinton Reading Rooms, Swinton, Malton North YO17 6SG
        if record.pollingstationnumber == "4":
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if record.housepostcode in [
            "YO13 9PT",
            "YO17 9LB",
            "YO17 9QY",
            "YO17 9RL",
            "YO41 1JF",
            "YO60 7HQ",
            "YO60 7NB",
            "YO62 6JA",
            "YO62 6PA",
            "YO62 6PE",
        ]:
            return None

        if uprn in [
            "10007633975",
            "10007630076",
            "10002318338",
        ]:
            return None

        return super().address_record_to_dict(record)
