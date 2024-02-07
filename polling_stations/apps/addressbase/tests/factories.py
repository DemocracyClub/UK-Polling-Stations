import factory
from addressbase.models import Address, UprnToCouncil


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    uprn = factory.Sequence(lambda n: f"{n}".zfill(9))
    addressbase_postal = "D"
    location = factory.Faker("geo_point", country_code="GB")


class UprnToCouncilFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UprnToCouncil

    uprn = factory.SubFactory(AddressFactory)
