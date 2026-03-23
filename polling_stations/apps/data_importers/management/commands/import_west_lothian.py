from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "WLN"
    addresses_name = "2026-05-07/2026-03-23T10:25:10.603421/lothian_vjb_combined.csv"
    stations_name = "2026-05-07/2026-03-23T10:25:10.603421/lothian_vjb_combined.csv"
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

        if uprn in []:
            return None

        if record.postcode in (
            # splits
            "EH47 7NL",
            "EH48 4JH",
            "EH48 2NX",
            "EH49 6QL",
            "EH48 2GT",
            "EH54 7FJ",
            "EH52 6PP",
            "EH53 0QW",
            "EH53 0UT",
            "EH49 6BQ",
            "EH52 5PJ",
            "EH54 9FH",
            "EH48 3JB",
            "EH47 9EA",
            "EH49 6BD",
        ):
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.pollingvenueid not in self.COUNCIL_STATIONS:
            return None

        return super().station_record_to_dict(record)
