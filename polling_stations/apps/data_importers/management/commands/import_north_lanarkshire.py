from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter
from django.template.defaultfilters import slugify


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "NLK"
    addresses_name = "2026-05-07/2026-03-18T09:20:01.974806/Democracy Club - Idox_2026-03-17 14-28.csv"
    stations_name = "2026-05-07/2026-03-18T09:20:01.974806/Democracy Club - Idox_2026-03-17 14-28.csv"
    elections = ["2026-05-07"]

    def get_station_hash(self, record):
        # Otherwise the masonic halls in Coatbridge get confused with each other
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
                self.COUNCIL_STATIONS.add(record.pollingvenueid)

    def address_record_to_dict(self, record):
        if record.pollingvenueid not in self.COUNCIL_STATIONS:
            return None

        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "118047509",  # 2 GYLE PLACE, WISHAW
            "118047511",  # 4 GYLE PLACE, WISHAW
            "118047512",  # 6 GYLE PLACE, WISHAW
        ]:
            return None

        if record.postcode in (
            # splits
            "G33 6GN",
            "ML1 3GE",
            "ML1 3FD",
            "G69 8BW",
            "G67 2AG",
            "ML2 8NB",
            "G69 0AG",
            "ML6 8HQ",
            "ML1 3JW",
            "ML1 2TD",
            "ML4 2RE",
            "G67 2DL",
            "G68 9DB",
            "ML5 5QH",
            "ML1 4TU",
            "ML4 1RF",
            "ML1 5TU",
            "ML6 7SE",
            "ML6 8LW",
            "G65 9NG",
            "ML6 9BA",
            "ML6 8QN",
            # suspect
            "ML6 7SR",  # DYKEHEAD ROAD, RIGGEND, AIRDRIE
        ):
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.pollingvenueid not in self.COUNCIL_STATIONS:
            return None

        # COMMUNITY EDUCATION CENTRE, 2 CLARK STREET, AIRDRIE ML6 6DQ
        if (
            self.get_station_hash(record)
            == "1-community-education-centre-2-clark-street-airdrie-"
        ):
            record = record._replace(pollingstationpostcode="")
        return super().station_record_to_dict(record)
