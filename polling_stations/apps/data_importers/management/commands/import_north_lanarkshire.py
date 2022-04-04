from django.template.defaultfilters import slugify

from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NLK"
    addresses_name = (
        "2022-05-05/2022-04-04T10:47:03.448532/polling_station_export-2022-03-23 2.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-04T10:47:03.448532/polling_station_export-2022-03-23 2.csv"
    )
    elections = ["2022-05-05"]

    def get_station_hash(self, record):
        # Otherwise the masonic halls in Coatbridge get confused with each other
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
            "ML1 3JW",
            "ML4 1RF",
            "ML1 1NQ",
            "G68 9DB",
            "ML4 2RE",
            "ML5 5QH",
            "G65 9NG",
            "ML1 2TD",
            "G67 2AG",
            "ML1 3GE",
            "G67 2DL",
            "ML6 8HQ",
            "ML6 8QN",
            "G69 8AA",
            "ML5 4FE",
            "G69 8BW",
            "G69 9JF",
            "ML2 9NG",
            "ML6 8LW",
            "ML6 9BA",
            "ML1 4TU",
            "ML6 7SE",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if self.get_station_hash(record) not in self.COUNCIL_STATIONS:
            return None

        if (
            self.get_station_hash(record)
            == "1-community-education-centre-2-clark-street-airdrie-"
        ):
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)
