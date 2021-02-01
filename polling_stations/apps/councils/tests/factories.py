import itertools
import string

import factory

from councils.models import Council, CouncilGeography


class CouncilGeographyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CouncilGeography


class CouncilFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Council

    council_id = factory.Iterator(itertools.product(string.ascii_uppercase, repeat=3))
    identifiers = factory.Sequence(lambda n: [f"E00000{n}"])
    geography = factory.RelatedFactory(
        CouncilGeographyFactory,
        factory_related_name="council",
        geography="MULTIPOLYGON (((-3.56956187 50.74486474, -3.55201052 50.7451411, -3.51226598 50.76110934, -3.50291102 50.75559155, -3.46073245 50.738483, -3.46238509 50.71596844, -3.47111128 50.69932895, -3.46127953 50.69369784, -3.45954629 50.6848728, -3.45664587 50.68205419, -3.45072202 50.68218075, -3.45667254 50.67325256, -3.46657471 50.68274835, -3.47693745 50.6840921, -3.48320458 50.68862345, -3.49274133 50.68889777, -3.49357574 50.69190159, -3.5017562 50.69433616, -3.50646081 50.69113946, -3.52381224 50.69295718, -3.52681725 50.69533169, -3.53011473 50.69280087, -3.5385489 50.6932753, -3.54026649 50.69483633, -3.54734585 50.70308832, -3.56278466 50.70747076, -3.56694759 50.71525985, -3.56462829 50.7180474, -3.56608774 50.72409107, -3.57020312 50.7278075, -3.56089305 50.73084906, -3.56956187 50.74486474)))",  # noqa
        gss=factory.LazyAttribute(lambda o: o.factory_parent.identifiers[0]),
    )
