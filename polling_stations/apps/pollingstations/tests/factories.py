import factory
from councils.tests.factories import CouncilFactory
from django.contrib.gis.geos import Point
from faker.providers import BaseProvider
from pollingstations.models import (
    AccessibilityInformation,
    AdvanceVotingStation,
    PollingDistrict,
    PollingStation,
)


class DjangoGeoPointProvider(BaseProvider):
    def geo_point(self, **kwargs):
        kwargs["coords_only"] = True
        kwargs["country_code"] = "GB"
        faker = factory.faker.faker.Faker()
        coords = faker.local_latlng(**kwargs)
        return Point(x=float(coords[1]), y=float(coords[0]), srid=4326)


factory.Faker.add_provider(DjangoGeoPointProvider)


class PollingStationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PollingStation

    council = factory.SubFactory(CouncilFactory)
    internal_council_id = factory.Sequence(lambda n: f"PS-{n}")


class AccessibilityInformationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccessibilityInformation

    polling_station = factory.SubFactory(PollingStationFactory)


class PollingDistrictFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PollingDistrict

    council = factory.SubFactory(CouncilFactory)
    internal_council_id = factory.Sequence(lambda n: f"PD-{n}")


class AdvanceVotingStationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AdvanceVotingStation

    name = factory.Faker("company", locale="en_GB")
    address = factory.Faker("address", locale="en_GB")
    postcode = factory.Faker("postcode", locale="en_GB")
    location = factory.Faker("geo_point", country_code="GB")
    council = factory.SubFactory(CouncilFactory)
