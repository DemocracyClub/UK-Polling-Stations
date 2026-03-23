from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter
from django.template.defaultfilters import slugify


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "SLK"
    addresses_name = "2026-05-07/2026-03-23T10:12:14.328561/SLK_combined.csv"
    stations_name = "2026-05-07/2026-03-23T10:12:14.328561/SLK_combined.csv"
    elections = ["2026-05-07"]

    def get_station_hash(self, record):
        # This prevents stations with the same name in the North Lanarkshire data from being mistaken for ones in South Lanarkshire
        return "-".join(
            [
                record.pollingstationnumber.strip(),
                slugify(record.pollingstationname.strip())[:60],
                slugify(record.pollingstationaddress1.strip()),
                slugify(record.pollingstationaddress2.strip()),
                slugify(record.pollingstationaddress3.strip()),
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

        if record.uprn in [
            "484131230",  # MUIRHOUSE FARM, THANKERTON, BIGGAR, ML12 6NJ
            "484140163",  # WOODLEA, THANKERTON, BIGGAR, ML12 6NF
            "484121979",  # BROOKFIELD, DEVONSIDE ROAD, CARMICHAEL, BIGGAR, ML12 6PQ
            "484180542",  # SEAFORTH COURTYARD, BRAIDWOOD, CARLUKE, ML8 5NE
            "484114775",  # HAWTHORN COTTAGE CARTLAND BRIDGE, LANARK, ML11 9UF
            "484017180",  # 184 GLENFRUIN ROAD, BLANTYRE, GLASGOW, G72 9RL
            "484011788",  # BARONHILL, HUNTHILL ROAD, BLANTYRE, GLASGOW, G72 9UY
        ]:
            return None

        if record.postcode in [
            # split
            "G74 4DF",
            "G72 8WN",
            "ML3 9GD",
            "G72 8FG",
            "G72 7NT",
            "ML11 0PG",
            "G75 8JW",
            "G73 4AP",
            "G72 7XQ",
            "ML10 6ET",
            "ML11 0BG",
            "G75 8ND",
            "ML12 6PP",
            "ML10 6FB",
            "ML12 6SW",
            "G71 7TD",
            "G71 8DG",
            # looks wrong
            "ML12 6JJ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if self.get_station_hash(record) not in self.COUNCIL_STATIONS:
            return None
        return super().station_record_to_dict(record)
