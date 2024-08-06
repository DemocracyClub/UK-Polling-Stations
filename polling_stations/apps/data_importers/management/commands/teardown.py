import random

from addressbase.models import UprnToCouncil
from councils.models import Council
from data_importers.event_helpers import record_teardown_event
from data_importers.models import DataQuality
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection, router, transaction
from pollingstations.models import AdvanceVotingStation, PollingDistrict, PollingStation
from rich.console import Console
from rich.prompt import Prompt

"""
Clear PollingDistrict, PollingStation, and AdvancedVotingStation models
Clear polling_station_id field in UprnToCouncil model
Clear report, num_addresses, num_districts and num_stations
fields in DataQuality model
"""


def check_is_prod_db():
    database_config = router.db_for_read(PollingStation)
    database_name = settings.DATABASES[database_config]["NAME"]

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT description
            FROM pg_shdescription
            JOIN pg_database ON pg_shdescription.objoid = pg_database.oid
            WHERE pg_database.datname = %s;
        """,
            [database_name],
        )
        comment = cursor.fetchone()
        if comment:
            return comment[0] == "env:production"
        return None


def confirm_teardown_on_prod():
    if check_is_prod_db():
        console = Console()
        token = [str(n) for n in random.sample(range(10), 5)]
        console.print(
            "WARNING: THIS IS A PRODUCTION DATABASE, CONTINUING WILL DELETE ALL DATA!",
            style="red on white",
        )

        verification_token = Prompt.ask(
            f"""Enter {' '.join(token)} without spaces to confirm"""
        )
        if verification_token == "".join(token):
            return True
        return False
    return True


class Command(BaseCommand):
    """
    Turn off auto system check for all apps
    We will maunally run system checks only for the
    'data_importers' and 'pollingstations' apps
    """

    requires_system_checks = []

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)

        group.add_argument(
            "-c",
            "--council",
            nargs=1,
            help="Council ID to clear in the format X01000001",
        )

        group.add_argument(
            "-a",
            "--all",
            help="Clear data for all councils (will completely ruin your database)",
            action="store_true",
            default=False,
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        """
        Manually run system checks for the
        'data_importers' and 'pollingstations' apps
        Management commands can ignore checks that only apply to
        the apps supporting the website part of the project
        """
        self.check(
            [
                apps.get_app_config("data_importers"),
                apps.get_app_config("pollingstations"),
            ]
        )

        if kwargs["council"]:
            for council_id in kwargs["council"]:
                print("Deleting data for council %s..." % (council_id))
                # check this council exists
                council_obj = Council.objects.get(pk=council_id)
                gss_code = council_obj.geography.gss

                PollingStation.objects.filter(council=council_id).delete()
                PollingDistrict.objects.filter(council=council_id).delete()
                AdvanceVotingStation.objects.filter(council=council_id).delete()

                UprnToCouncil.objects.filter(lad=gss_code).update(polling_station_id="")

                dq = DataQuality.objects.get(council_id=council_id)
                dq.report = ""
                dq.num_addresses = 0
                dq.num_districts = 0
                dq.num_stations = 0
                dq.save()

                record_teardown_event(council_id)
                print("..done")

        elif kwargs.get("all"):
            if not confirm_teardown_on_prod():
                print("Stopping")
                return

            print("Deleting ALL data...")
            for council in Council.objects.with_polling_stations_in_db():
                record_teardown_event(council.council_id)
            PollingDistrict.objects.all().delete()
            PollingStation.objects.all().delete()
            AdvanceVotingStation.objects.all().delete()

            UprnToCouncil.objects.exclude(polling_station_id="").update(
                polling_station_id=""
            )
            DataQuality.objects.all().update(
                report="", num_addresses=0, num_districts=0, num_stations=0
            )
            print("..done")
