from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ANS"
    addresses_name = "2026-06-18/2026-05-28T15:29:36.811918/Democracy Club - Idox_2026-05-28 14-58.csv"
    stations_name = "2026-06-18/2026-05-28T15:29:36.811918/Democracy Club - Idox_2026-05-28 14-58.csv"
    elections = ["2026-06-18"]

    def address_record_to_dict(self, record):
        if record.postcode in [
            # splits
            "DD8 2TJ",
        ]:
            return None

        return super().address_record_to_dict(record)

    # maintaining some corrections through by-election
    # def station_record_to_dict(self, record):
    #     # add missing postcode for: Glamis Heritage Education Centre, Glamis
    #     if record.pollingstationnumber == "80":
    #         record = record._replace(pollingstationpostcode="DD8 1RS")

    #     # add missing postcode for: Kingoldrum Village Hall, Kingoldrum
    #     if record.pollingstationnumber == "70":
    #         record = record._replace(pollingstationpostcode="DD8 5HW")

    #     return super().station_record_to_dict(record)
