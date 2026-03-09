from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "ABD"
    addresses_name = "2026-05-07/2026-03-16T11:46:46.121836/ABD_combined_2.csv"
    stations_name = "2026-05-07/2026-03-16T11:46:46.121836/ABD_combined_2.csv"
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

        if (
            uprn
            in [
                "151176475",  # CARAVAN 5 DYKELANDS FARM A937 SOUTH BALMAKELLY ACCESS ROAD TO A90T SOUTH OF LAURENCEKIRK, LAURENCEKIRK
            ]
        ):
            return None

        if record.postcode in (
            # splits
            "AB51 8XH",
            "AB43 7AR",
            "AB35 5PR",
            "AB51 0UZ",
            "AB21 0QJ",
            "AB41 7UA",
            "AB42 5JB",
            "AB39 2UJ",
        ):
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.pollingvenueid not in self.COUNCIL_STATIONS:
            return None
        # Remove station in Aberdeen City
        if record.pollingvenueid == "108":
            return None
        # corrects wrong postcode for: TOWIE PUBLIC HALL, TOWIE, GLENKINDIE, ALFORD AB33 8NR
        if self.get_station_hash(record) == "44-towie-public-hall":
            record = record._replace(pollingstationpostcode="AB33 8RN")

        return super().station_record_to_dict(record)
