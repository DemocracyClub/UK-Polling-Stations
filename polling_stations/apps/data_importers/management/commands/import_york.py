from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "YOR"
    addresses_name = (
        "2023-05-04/2023-05-04T11:51:02.449124/DemocracyClub_PollingDistricts.csv"
    )
    stations_name = (
        "2023-05-04/2023-05-04T11:51:02.449124/DemocracyClub_PollingStations.csv"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "YO19 6BG",
        ]:
            return None
        if record.uprn in [
            "",
        ]:
            return None
        return super().address_record_to_dict(record)
