from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "NAY"
    addresses_name = (
        "2026-05-07/2026-03-24T15:05:48.405682/Democracy club - Polling Districts.csv"
    )
    stations_name = (
        "2026-05-07/2026-03-24T15:05:48.405682/Democracy club - Polling Stations.csv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

    def pre_import(self):
        # We need to consider rows that don't have a uprn when importing data.
        # However there are lots of rows for other councils in this file.
        # So build a list of stations from rows that do have UPRNS
        # and then use that list of stations to make sure we check relevant rows, even if they don't have a UPRN

        council_uprns = set(
            UprnToCouncil.objects.exclude(
                uprn__in=[
                    "126087302",  # in NAY, but assigned to station in EAY
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

        uprn = record.uprn.strip().lstrip("0")
        if uprn in [
            "126092854",  # 4 EILEAN CLOSE, LAMLASH, ISLE OF ARRAN
            "126060794",  # LONGFORD COTTAGE, NETHERMAINS ROAD, KILWINNING
        ]:
            return None

        if record.postcode in [
            # suspect
            "KA11 2HG",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.stationcode not in self.COUNCIL_STATIONS:
            return None

        return super().station_record_to_dict(record)
