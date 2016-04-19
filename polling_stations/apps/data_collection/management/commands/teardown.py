from django.core.management.base import BaseCommand
from django.db import connection
from pollingstations.models import PollingStation, PollingDistrict, ResidentialAddress

"""
Clear PollingDistrict, PollingStation and ResidentialAddress models
Clear report, num_addresses, num_districts and num_stations
fields in DataQuality model
"""
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        PollingDistrict.objects.all().delete()
        PollingStation.objects.all().delete()
        ResidentialAddress.objects.all().delete()
        # use raw SQL so we don't have to loop over every single record one-by-one
        cursor = connection.cursor()
        cursor.execute("UPDATE data_collection_dataquality SET report='', num_addresses=0, num_districts=0, num_stations=0")
