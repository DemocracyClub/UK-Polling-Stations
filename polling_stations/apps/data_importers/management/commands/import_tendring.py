from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "TEN"
    addresses_name = (
        "2024-07-04/2024-06-04T09:33:44.379451/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-04T09:33:44.379451/Democracy Club - Polling Stations.csv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.postcode in [
            # suspect
            "CO15 1HW",
            "CO15 3BN",
            "CO15 1JG",
            "CO15 1JL",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # dirty workaround to remove 32 Colchester stations with no addresses assigned
        # these records are ordered, we can just exclude them by station_code
        if int(record.stationcode) > 77:
            return None

        return super().station_record_to_dict(record)
