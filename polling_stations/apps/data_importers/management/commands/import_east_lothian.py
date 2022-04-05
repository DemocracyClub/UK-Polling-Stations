from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ELN"
    addresses_name = (
        "2022-05-05/2022-03-09T09:53:53.386346/polling_station_export-2022-03-02 2.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-09T09:53:53.386346/polling_station_export-2022-03-02 2.csv"
    )
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
            "EH31 2B",
            "EH32 0LN",
            "EH31 2HS",
            "EH21 8F",
            "EH35 5ND",
            "EH32 0F",
            "EH39 5EY",
            "EH41 4DQ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if self.get_station_hash(record) not in self.COUNCIL_STATIONS:
            return None

        return super().station_record_to_dict(record)
