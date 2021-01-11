import itertools
import string

import factory

from councils.models import Council


class CouncilFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Council

    council_id = factory.Iterator(itertools.product(string.ascii_uppercase, repeat=3))
