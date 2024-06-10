from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRO"
    addresses_name = (
        "2024-07-04/2024-06-10T16:27:26.619923/SNOandBRO_districts_combined.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-10T16:27:26.619923/SNOandBRO_stations_combined.csv"
    )
    elections = ["2024-07-04"]

    def pre_import(self):
        # We need to consider rows that don't have a uprn when importing data.
        # However there are lots of rows for other councils in this file.
        # So build a list of stations from rows that do have UPRNS
        # and then use that list of stations to make sure we check relevant rows, even if they don't have a UPRN

        council_uprns = set(
            UprnToCouncil.objects.filter(lad=self.council.geography.gss).values_list(
                "uprn", flat=True
            )
        )
        self.COUNCIL_STATIONS = set()
        data = self.get_addresses()

        for record in data:
            if record.uprn in council_uprns:
                self.COUNCIL_STATIONS.add(record.stationcode)

    def station_record_to_dict(self, record):
        if record.stationcode not in self.COUNCIL_STATIONS:
            return None

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.stationcode not in self.COUNCIL_STATIONS:
            return None

        uprn = record.uprn.lstrip("0").strip()

        if uprn in [
            "10009923018",  # THE BUNGALOW, THE HEATH, HEVINGHAM, NORWICH
        ]:
            return None

        if record.postcode in [
            "NR7 0RY",  # split
        ]:
            return None
        return super().address_record_to_dict(record)
