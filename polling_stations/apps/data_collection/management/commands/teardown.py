from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection
from pollingstations.models import PollingStation, PollingDistrict, ResidentialAddress

"""
Clear PollingDistrict, PollingStation and ResidentialAddress models
Clear report, num_addresses, num_districts and num_stations
fields in DataQuality model
"""
class Command(BaseCommand):

    """
    Turn off auto system check for all apps
    We will maunally run system checks only for the
    'data_collection' and 'pollingstations' apps
    """
    requires_system_checks = False

    def handle(self, *args, **kwargs):
        """
        Manually run system checks for the
        'data_collection' and 'pollingstations' apps
        Management commands can ignore checks that only apply to
        the apps supporting the website part of the project
        """
        self.check([
            apps.get_app_config('data_collection'),
            apps.get_app_config('pollingstations')
        ])

        PollingDistrict.objects.all().delete()
        PollingStation.objects.all().delete()
        ResidentialAddress.objects.all().delete()
        # use raw SQL so we don't have to loop over every single record one-by-one
        cursor = connection.cursor()
        cursor.execute("UPDATE data_collection_dataquality SET report='', num_addresses=0, num_districts=0, num_stations=0")
