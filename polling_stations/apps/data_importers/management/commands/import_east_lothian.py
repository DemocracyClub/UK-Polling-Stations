from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "ELN"
    addresses_name = "2026-05-07/2026-03-23T10:20:31.527981/lothian_vjb_combined.csv"
    stations_name = "2026-05-07/2026-03-23T10:20:31.527981/lothian_vjb_combined.csv"
    elections = ["2026-05-07"]

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
                self.COUNCIL_STATIONS.add(record.pollingvenueid)

    def address_record_to_dict(self, record):
        if record.pollingvenueid not in self.COUNCIL_STATIONS:
            return None

        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "138000991",  # SEAFIELD HOUSE, EAST LINKS ROAD, DUNBAR
            "138007056",  # 94 HIGH STREET, COCKENZIE, PRESTONPANS
            "138072115",  # 30 SMEATON GARDENS, WHITECRAIG, MUSSELBURGH
        ]:
            return None

        if record.postcode in (
            # splits
            "EH32 0LN",
            "EH41 4DQ",
            "EH32 0FL",
            "EH21 6TB",
            "EH21 6TF",
            "EH31 2HS",
            "EH42 1ZL",
            "EH21 8EJ",
            "EH33 2PT",
            "EH32 9GH",
            "EH35 5ND",
            "EH39 5EY",
        ):
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.pollingvenueid not in self.COUNCIL_STATIONS:
            return None

        return super().station_record_to_dict(record)
