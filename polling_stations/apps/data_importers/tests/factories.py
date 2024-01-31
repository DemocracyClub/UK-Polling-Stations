import factory
from data_importers.models import DataEvent


class DataEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DataEvent
