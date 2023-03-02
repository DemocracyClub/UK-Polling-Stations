from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRO"
    addresses_name = "2023-05-04/2023-03-02T16:21:01.206095/DemocracyClub-PollingDistricts-May2023-1.csv"
    stations_name = "2023-05-04/2023-03-02T16:21:01.206095/DemocracyClub-PollingStations-May2023-1.csv"
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        if record.stationcode.startswith("S"):
            return None
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.stationcode.startswith("S"):
            return None

        if record.postcode in [
            "NR7 0RY",
            "NR13 3NQ",
        ]:  # split
            return None

        uprn = record.uprn.lstrip("0").strip()

        if uprn in [
            "10009923018",  # THE BUNGALOW, THE HEATH, HEVINGHAM, NORWICH
        ]:
            return None

        return super().address_record_to_dict(record)
