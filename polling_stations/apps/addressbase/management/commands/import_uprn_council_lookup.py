from django.db import connection
from django.core.management.base import BaseCommand
from pathlib import Path


class Command(BaseCommand):
    """
    Command to import a csv which maps UPRNs to Local Authority GSS codes.
    The csv should have two columns: 'uprn' and 'lad'.
    You probably want to generate it with 'create_uprn_council_lookup'.
    """

    def add_arguments(self, parser):
        parser.add_argument("path", help="Path to CSV mapping UPRNs to GSS codes.")

    def handle(self, *args, **kwargs):
        self.path = Path(kwargs["path"])
        self.table_name = "addressbase_uprntocouncil"

        if not self.path.exists():
            raise FileNotFoundError(f"No csv found at {kwargs['path']}")

        cursor = connection.cursor()
        self.stdout.write("clearing existing data..")
        cursor.execute("TRUNCATE TABLE %s;" % (self.table_name))

        self.stdout.write("importing from CSV..")
        with self.path.open("r") as f:
            cursor.copy_from(f, self.table_name, sep=",")

        self.stdout.write("...done")
