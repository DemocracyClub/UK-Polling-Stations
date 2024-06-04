from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.template.defaultfilters import slugify


class Command(BaseHalaroseCsvImporter):
    council_id = "NLK"
    addresses_name = "2024-07-04/2024-06-12T11:58:06.789209/NLK_combined.csv"
    stations_name = "2024-07-04/2024-06-12T11:58:06.789209/NLK_combined.csv"
    elections = ["2024-07-04"]

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

    def station_record_to_dict(self, record):
        if self.get_station_hash(record) not in self.COUNCIL_STATIONS:
            return None

        # COMMUNITY EDUCATION CENTRE, 2 CLARK STREET, AIRDRIE ML6 6DQ
        if (
            self.get_station_hash(record)
            == "1-community-education-centre-2-clark-street-airdrie-"
        ):
            record = record._replace(pollingstationpostcode="")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if self.get_station_hash(record) not in self.COUNCIL_STATIONS:
            return None

        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "118047509",  # 2 GYLE PLACE, WISHAW
            "118047511",  # 4 GYLE PLACE, WISHAW
            "118047512",  # 6 GYLE PLACE, WISHAW
        ]:
            return None

        if record.housepostcode in [
            # split
            "ML4 1RF",
            "ML1 3FD",
            "G67 2DL",
            "ML6 8HQ",
            "ML1 3GE",
            "ML1 3JW",
            "ML5 5QH",
            "ML1 2TD",
            "ML1 4TU",
            "ML6 9BA",
            "G69 8BW",
            "ML6 8QN",
            "G65 9NG",
            "ML4 2RE",
            "G33 6GN",
            "ML1 2BP",
            "ML6 7SE",
            "ML2 9NG",
            "G69 9JF",
            "G67 2AG",
            "ML6 8LW",
            "G68 9DB",
            "ML6 8JE",
            # suspect
            "ML6 7SR",  # DYKEHEAD ROAD, RIGGEND, AIRDRIE
            "G67 1JE",
            "G67 1JQ",
            "G67 1JB",
            "G67 1JG",
            "G67 1JJ",
            "G67 1JN",
            "G67 1JF",
            "G67 1JL",
            "G67 1JH",
            "G67 1JD",
        ]:
            return None

        return super().address_record_to_dict(record)
