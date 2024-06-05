from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ELN"
    addresses_name = "2024-07-04/2024-06-13T12:31:53.064062/ELN_combined_UTF-8.csv"
    stations_name = "2024-07-04/2024-06-13T12:31:53.064062/ELN_combined_UTF-8.csv"
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
            # removes: Summerside Bowling Club 21 Summerside Street
            if self.get_station_hash(record) == "112-summerside-bowling-club":
                continue
            if record.uprn in council_uprns:
                self.COUNCIL_STATIONS.add(self.get_station_hash(record))

    def address_record_to_dict(self, record):
        if self.get_station_hash(record) not in self.COUNCIL_STATIONS:
            return None

        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "138068895",  # 22 MEADOWSIDE, ABERLADY, LONGNIDDRY
        ]:
            return None

        if record.housepostcode in [
            # split
            "EH41 4DQ",
            "EH35 5ND",
            "EH21 8EJ",
            "EH31 2HS",
            "EH21 6TB",
            "EH32 0LN",
            "EH39 5EY",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if self.get_station_hash(record) not in self.COUNCIL_STATIONS:
            return None

        return super().station_record_to_dict(record)
