import factory

from councils.tests.factories import CouncilFactory
from pollingstations.models import PollingStation, PollingDistrict


class PollingStationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PollingStation

    council = factory.SubFactory(CouncilFactory)
    internal_council_id = factory.Sequence(lambda n: f"PS-{n}")


class PollingDistrictFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PollingDistrict

    council = factory.SubFactory(CouncilFactory)
    internal_council_id = factory.Sequence(lambda n: f"PD-{n}")
