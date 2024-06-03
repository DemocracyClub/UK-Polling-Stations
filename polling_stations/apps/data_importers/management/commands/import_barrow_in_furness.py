from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BAR"
    addresses_name = "2024-07-04/2024-06-03T14:37:33.938121/WandF_3_in_1.csv"
    stations_name = "2024-07-04/2024-06-03T14:37:33.938121/WandF_3_in_1.csv"
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
                station_hash = self.get_station_hash(record)
                self.COUNCIL_STATIONS.add(station_hash)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        station_hash = self.get_station_hash(record)
        if station_hash not in self.COUNCIL_STATIONS:
            return None

        if uprn in [
            "10096612357",  # ROOM 3 2 ALLISON STREET, BARROW-IN-FURNESS
        ]:
            return None

        if record.housepostcode in [
            # split
            "LA14 4QJ",
            "LA13 9SF",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        station_hash = self.get_station_hash(record)
        if station_hash not in self.COUNCIL_STATIONS:
            return None
        return super().station_record_to_dict(record)
