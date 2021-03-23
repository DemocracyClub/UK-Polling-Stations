from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NEL"
    addresses_name = "2021-03-11T16:28:19.988914/polling_station_export-2021-03-11.csv"
    stations_name = "2021-03-11T16:28:19.988914/polling_station_export-2021-03-11.csv"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        # https://trello.com/c/kXIT1oFl/380-north-east-lincolnshire
        if record.pollingstationname == "HABROUGH VILLAGE HALL":
            record = record._replace(pollingstationpostcode="DN40 3BD")
        return super().station_record_to_dict(record)
