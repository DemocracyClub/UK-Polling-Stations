from addressbase.models import UprnToCouncil
from councils.models import Council
from data_importers.models import DataQuality
from django.apps import apps
from django.core.management.base import BaseCommand
from pollingstations.models import AdvanceVotingStation, PollingDistrict, PollingStation

"""
Clear PollingDistrict, PollingStation, and AdvancedVotingStation models
Clear polling_station_id field in UprnToCouncil model
Clear report, num_addresses, num_districts and num_stations
fields in DataQuality model
"""


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
                print("..done")

        elif kwargs.get("all"):
            print("Deleting ALL data...")
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
