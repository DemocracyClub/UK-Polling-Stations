from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SLK"
    addresses_name = "2024-07-04/2024-06-12T14:52:20.607722/SLK_combined_v2.csv"
    stations_name = "2024-07-04/2024-06-12T14:52:20.607722/SLK_combined_v2.csv"
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
                self.COUNCIL_STATIONS.add(self.get_station_hash(record))

    def station_record_to_dict(self, record):
        if self.get_station_hash(record) not in self.COUNCIL_STATIONS:
            return None
        # Removing one the stations at the following polling place until the council responds:
        # St Bride's Primary School (Nursery Entrance), Tabernacle Street, Cambuslang G72 8JN
        if (
            self.get_station_hash(record)
            == "262-st-brides-primary-school-nursery-entrance"
        ):
            return None
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if self.get_station_hash(record) not in self.COUNCIL_STATIONS:
            return None

        # Removing the addresses assigned to one of the stations at the following polling place until the council responds:
        # St Bride's Primary School (Nursery Entrance), Tabernacle Street, Cambuslang G72 8JN
        if (
            self.get_station_hash(record)
            == "262-st-brides-primary-school-nursery-entrance"
        ):
            return None

        if record.housepostcode in [
            # split
            "G75 8HZ",
            "ML3 6UG",
            "ML12 6PP",
            "G74 4DF",
            "G72 7NT",
            "G71 7TD",
            "ML3 7QW",
            "G72 8WN",
            "G75 8JW",
            "ML10 6ET",
            "ML12 6SW",
            "G71 8DG",
            "ML11 0BG",
            "G72 8FG",
            "ML10 6FB",
            "G75 8ND",
            "G73 4AP",
            "ML11 0PG",
            "G72 7XQ",
        ]:
            return None

        return super().address_record_to_dict(record)
