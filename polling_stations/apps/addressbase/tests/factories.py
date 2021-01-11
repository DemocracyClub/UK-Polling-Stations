import factory

from addressbase.models import Address, UprnToCouncil


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    uprn = factory.Sequence(lambda n: f"{n}".zfill(9))
    addressbase_postal = "D"


class UprnToCouncilFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UprnToCouncil

    uprn = factory.SubFactory(AddressFactory)
