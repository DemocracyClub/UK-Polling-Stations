from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ABD"
    addresses_name = "2022-05-05/2022-04-12T10:11:25.128402/polling_station_export-2022-04-07.edited.csv"
    stations_name = "2022-05-05/2022-04-12T10:11:25.128402/polling_station_export-2022-04-07.edited.csv"
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
            "AB39 2UJ",
            "AB30 1SL",
            "AB43 7LN",
            "AB42 5JB",
            "AB51 8XH",
            "AB41 7UA",
            "AB51 5DU",
            "AB21 0QJ",
            "AB35 5PR",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        station_hash = self.get_station_hash(record)
        if station_hash not in self.COUNCIL_STATIONS:
            return None

        if station_hash == "74-hanover-community-centre":
            return None

        return super().station_record_to_dict(record)
