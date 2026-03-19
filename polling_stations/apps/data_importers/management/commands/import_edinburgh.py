from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "EDH"
    addresses_name = "2026-05-07/2026-03-23T10:18:05.702679/lothian_vjb_combined.csv"
    stations_name = "2026-05-07/2026-03-23T10:18:05.702679/lothian_vjb_combined.csv"
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

        if record.postcode in (
            # splits
            "EH4 4TN",
            "EH16 5DZ",
            "EH11 1JU",
            "EH16 5AU",
            "EH16 5FB",
            "EH13 0DA",
            "EH6 7FN",
            "EH6 8DQ",
            "EH29 9FQ",
            "EH16 4TW",
            "EH16 6XE",
            "EH17 8HU",
            "EH15 1RB",
        ):
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.pollingvenueid not in self.COUNCIL_STATIONS:
            return None

        return super().station_record_to_dict(record)
