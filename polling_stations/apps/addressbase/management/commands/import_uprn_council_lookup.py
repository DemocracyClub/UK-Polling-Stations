from pathlib import Path

from addressbase.models import Address, UprnToCouncil
from django.core.management.base import BaseCommand
from polling_stations.db_routers import get_principal_db_connection


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

        cursor = get_principal_db_connection().cursor()
        self.stdout.write("clearing existing data..")
        cursor.execute("TRUNCATE TABLE %s;" % (self.table_name))

        self.stdout.write("importing from CSV..")
        with self.path.open("r") as f:
            cursor.copy_from(f, self.table_name, sep=",")

        self.stdout.write("...done")
        self.stdout.write(
            "Looking for addresses outside council areas... (aka the pier check...)"
        )
        for address in Address.objects.filter(uprntocouncil__isnull=True):
            council = address.get_council_from_others_in_postcode()
            if council:
                self.stdout.write(
                    f"Creating UprnToCouncil record for {address.uprn} with gss {council.geography.gss}"
                )
                UprnToCouncil.objects.create(
                    uprn=address, lad=council.geography.gss, polling_station_id=""
                )
            else:
                self.stdout.write(f"Council ambiguous for {address.uprn}, deleting")
                address.delete()
