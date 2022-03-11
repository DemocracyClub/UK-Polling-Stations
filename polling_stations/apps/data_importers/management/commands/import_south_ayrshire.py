from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SAY"
    addresses_name = "2022-05-05/2022-03-11T15:12:43.190348/Democracy Club Polling Districts Ayrshire.csv"
    stations_name = "2022-05-05/2022-03-11T15:12:43.190348/Democracy Club Polling Stations Ayrshire.csv"
    elections = ["2022-05-05"]

    def pre_import(self):
        # We need to consider rows that don't have a uprn when importing data.
        # However there are lots of rows for other councils in this file.
        # So build a list of stations from rows that do have UPRNS
        # and then use that list of stations to make sure we check relevant rows, even if they don't have a UPRN

        council_uprns = set(
            UprnToCouncil.objects.exclude(
                uprn__in=[
                    "141045107",  # in SAY, but assigned to station in EAY
                    "141040335",  # in SAY, but assigned to station in EAY
                ]
            )
            .filter(lad=self.council.geography.gss)
            .values_list("uprn", flat=True)
        )
        self.COUNCIL_STATIONS = set()
        data = self.get_addresses()

        for record in data:
            if record.uprn in council_uprns:
                self.COUNCIL_STATIONS.add(record.stationcode)

    def address_record_to_dict(self, record):
        if record.stationcode not in self.COUNCIL_STATIONS:
            return None

        if record.postcode in [
            "KA6 6LU",
            "KA1 5QR",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.stationcode not in self.COUNCIL_STATIONS:
            return None

        return super().station_record_to_dict(record)
