from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SNO"
    addresses_name = "2023-05-04/2023-03-02T16:39:18.229053/DemocracyClub-PollingDistricts-May2023-1.csv"
    stations_name = "2023-05-04/2023-03-02T16:39:18.229053/DemocracyClub-PollingStations-May2023-1.csv"
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        if record.stationcode.startswith("B"):
            return None
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.stationcode.startswith("B"):
            return None
        return super().address_record_to_dict(record)
