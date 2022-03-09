from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WDU"
    addresses_name = "2022-05-05/2022-03-09T10:30:08.679838/polling_station_export-2022-03-02-3.csv 9th.csv"
    stations_name = "2022-05-05/2022-03-09T10:30:08.679838/polling_station_export-2022-03-02-3.csv 9th.csv"
    elections = ["2022-05-05"]

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
                self.COUNCIL_STATIONS.add(self.get_station_hash(record))

    def address_record_to_dict(self, record):
        if self.get_station_hash(record) not in self.COUNCIL_STATIONS:
            return None

        if record.housepostcode in [
            "G81 5AW",
            "G82 3EY",
            "G82 3LE",
            "G82 4JS",
            "G81 3PY",
            "G60 5DP",
        ]:
            return None

        if record.uprn in [
            "129058513",  # 53 CASTLEGATE AVENUE, DUMBARTON, G82 1AL
            "129048743",  # HIGHDYKES FARM, STIRLING ROAD, MILTON, DUMBARTON
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if self.get_station_hash(record) not in self.COUNCIL_STATIONS:
            return None

        return super().station_record_to_dict(record)
