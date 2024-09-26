import csv
from pathlib import Path

from addressbase.models import Address
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    This duplicates a csv but only taking uprns that are in our database
    It currently only works for Xpress
    It was used to generate csvs for testing as found in the test_data/pollingstations_data
    directory in the repository root.
    """

    def add_arguments(self, parser):
        parser.add_argument("source", help="Path to read csv from", default=None)
        parser.add_argument("destination", help="Path to write csv to", default=None)

    def handle(self, *args, **kwargs):
        self.source_path = Path(kwargs["source"])
        if not self.source_path.exists():
            raise FileNotFoundError(f"No csv found at {kwargs['path']}")
        self.destination_path = Path(kwargs["destination"])
        with self.source_path.open("r") as source_csv:
            dialect = csv.Sniffer().sniff(source_csv.read(4096))
            source_csv.seek(0)
            csv_reader = csv.DictReader(source_csv, dialect=dialect)
            fieldnames = csv_reader.fieldnames
            with self.destination_path.open("w") as destination_csv:
                csv_writer = csv.DictWriter(destination_csv, fieldnames=fieldnames)
                csv_writer.writeheader()
                for row in csv_reader:
                    try:
                        Address.objects.get(uprn=row["Property_URN"])
                        row["Polling_Place_Name"] = (
                            f'[TESTING]{row["Polling_Place_Name"]}[TESTING]'
                        )
                        csv_writer.writerow(row)
                    except Address.DoesNotExist:
                        continue
