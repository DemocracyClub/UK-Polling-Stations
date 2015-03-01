from django.apps import AppConfig
from django.db.models.signals import post_migrate

from .models import DataQuality
from councils.models import Council

def link_to_councils(sender, **kwargs):
    for council in Council.objects.all():
        DataQuality.objects.update_or_create(
            council=council,
        )




class DataFinder(AppConfig):
    name = 'data_finder'
    verbose_name = "Data Finder"
    def ready(self):
        post_migrate.connect(link_to_councils, sender=self)


