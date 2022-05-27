import csv
from pathlib import Path

from addressbase.models import UprnToCouncil
from django.core.management.base import BaseCommand

from councils.models import Council

NATIONS = {"E": "England", "N": "Northern Ireland", "S": "Scotland", "W": "Wales"}
NI_COUNCIL_NAMES = {
    "BFS": "Belfast City Council",
    "CCG": "Causeway Coast and Glens Borough Council",
    "NMD": "Newry, Mourne and Down District Council",
    "DRS": "Derry City and Strabane District Council",
    "FMO": "Fermanagh and Omagh District Council",
    "AND": "Ards and North Down Borough Council",
    "ANN": "Antrim and Newtownabbey Borough Council",
    "ABC": "Armagh City, Banbridge and Craigavon Borough Council",
    "LBC": "Lisburn and Castlereagh City Council",
    "MUL": "Mid Ulster District Council",
    "MEA": "Mid and East Antrim Borough Council",
}


class Command(BaseCommand):
    requires_system_checks = []

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            "--path",
            help="path to csv of feedbacks",
        )

    def handle(self, **options):
        csv_path = Path(options["path"])
        out_rows = []
        with open(csv_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                uprn = row["source_url"].replace("/address/", "").replace("/", "")
                try:
                    council = Council.objects.get(
                        geography__gss=UprnToCouncil.objects.get(uprn=uprn).lad
                    )
                    row["council_id"] = council.council_id
                    row["council_name"] = NI_COUNCIL_NAMES.get(
                        council.council_id, council.name
                    )
                    row["nation"] = NATIONS[council.geography.gss[0]]
                except UprnToCouncil.DoesNotExist:
                    print(f"{uprn} not found")
                    row["council_id"] = ""
                    row["council_name"] = ""
                    row["nation"] = ""

                out_rows.append(row)

        with open("feedback_councils.csv", "w", newline="") as outfile:
            fieldnames = out_rows[0].keys()
            writer = csv.DictWriter(outfile, dialect="excel", fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(out_rows)
        self.stdout.write("..done")
