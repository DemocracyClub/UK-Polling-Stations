from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.utils.text import slugify


class Command(BaseHalaroseCsvImporter):
    council_id = "SLK"
    addresses_name = (
        "2022-05-05/2022-04-04T10:48:38.156237/polling_station_export-2022-03-23 2.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-04T10:48:38.156237/polling_station_export-2022-03-23 2.csv"
    )
    elections = ["2022-05-05"]

    def get_station_hash(self, record):
        # Necessary in NLK, used here to be on the safe side.
        # eg distinguishes multiple 'St Mary's Primary School'
        return "-".join(
            [
                record.pollingstationnumber.strip(),
                slugify(record.pollingstationname.strip())[:60],
                slugify(record.pollingstationaddress_1.strip()),
                slugify(record.pollingstationaddress_2.strip()),
                slugify(record.pollingstationaddress_3.strip()),
            ]
        )[:100]

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
            "G71 8DG",
            "G72 7NT",
            "G75 8JW",
            "ML10 6FB",
            "G71 8FP",
            "G74 3ZD",
            "G72 9AJ",
            "ML12 6PP",
            "ML11 0BG",
            "G75 8ND",
            "G74 4DF",
            "ML12 6SW",
            "ML11 0PG",
            "ML3 7TF",
            "G72 7XQ",
            "G72 8FG",
            "G71 7TD",
            "G72 8WN",
            "ML3 7QW",
            "G73 4AP",
            "ML8 5LG",
            "ML11 9BX",
            "ML10 6ET",
            "ML11 9TS",
            "ML11 8PB",
            "ML3 7UU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if self.get_station_hash(record) not in self.COUNCIL_STATIONS:
            return None

        return super().station_record_to_dict(record)
