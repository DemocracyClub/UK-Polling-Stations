from addressbase.models import UprnToCouncil
from councils.models import Council
from data_importers.event_helpers import record_teardown_event
from data_importers.models import DataQuality
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction
from pollingstations.models import AdvanceVotingStation, PollingDistrict, PollingStation
from polling_stations.settings.constants.councils import NIR_IDS
from polling_stations.db_routers import get_principal_db_name

DB_NAME = get_principal_db_name()


class Command(BaseCommand):
    """
    Clear PollingDistrict, PollingStation, and AdvancedVotingStation models
    Clear polling_station_id field in UprnToCouncil model
    Clear report, num_addresses, num_districts and num_stations
    fields in DataQuality model
    """

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
            nargs="+",
            help="Council IDs to clear, uses three letter council codes, e.g. 'ABC'",
        )

        group.add_argument(
            "-a",
            "--all",
            help="Clear data for all councils (will completely ruin your database)",
            action="store_true",
            default=False,
        )

        group.add_argument(
            "--eoni",
            help="Clear data for all councils in Northern Ireland",
            action="store_true",
        )

    @transaction.atomic(using=DB_NAME)
    def teardown_councils(self, councils):
        for council in councils:
            self.stdout.write(
                f"Deleting data for: {council.name} ({council.council_id})..."
            )

        council_ids = [c.council_id for c in councils]
        gss_codes = [c.geography.gss for c in councils]

        PollingStation.objects.filter(council__in=council_ids).delete()
        PollingDistrict.objects.filter(council__in=council_ids).delete()
        AdvanceVotingStation.objects.filter(council__in=council_ids).delete()

        UprnToCouncil.objects.filter(lad__in=gss_codes).update(polling_station_id="")

        DataQuality.objects.filter(council_id__in=council_ids).update(
            report="",
            num_addresses=0,
            num_districts=0,
            num_stations=0,
        )

        for council_id in council_ids:
            record_teardown_event(council_id)

        self.stdout.write("..done")

    @transaction.atomic(using=DB_NAME)
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
            councils = Council.objects.all().filter(council_id__in=kwargs["council"])
            in_ids = set(kwargs["council"])
            db_ids = set([c.council_id for c in councils])
            if in_ids != db_ids:
                raise Exception(f"Could not find Council IDs: {in_ids-db_ids}")
            self.teardown_councils(councils)

        elif kwargs.get("eoni"):
            councils = Council.objects.all().filter(council_id__in=NIR_IDS)
            self.teardown_councils(councils)

        elif kwargs.get("all"):
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
