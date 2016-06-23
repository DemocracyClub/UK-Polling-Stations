from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from pollingstations.models import PollingStation, PollingDistrict
from councils.models import Council


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        #SCambs
        ps = PollingStation.objects.get(
            internal_council_id='PD1', council_id='E07000012')
        ps.postcode = "CB3 9NW"
        ps.address = "Grantchester Communal Centre, Tabrum Close, Grantchester"
        ps.location = None
        ps.save()

        ps = PollingStation.objects.get(
            internal_council_id='OC1', council_id='E07000012')
        ps.postcode = "CB24 6BL"
        ps.address = "Milton Community Centre, Coles Road, Milton, Cambridge"
        ps.location = None
        ps.save()

        ps = PollingStation.objects.get(
            internal_council_id='OC2', council_id='E07000012')
        ps.postcode = "CB24 6BL"
        ps.address = "Milton Community Centre, Coles Road, Milton, Cambridge"
        ps.location = None
        ps.save()

        c = Council.objects.get(council_id='E09000014')
        c.phone = "0208 489 1000"
        c.save()

        c = Council.objects.get(council_id='E06000006')
        c.phone = "0303 333 4300"
        c.save()

        ps = PollingStation.objects.get(internal_council_id='WH4P',
            council_id='E09000030')
        ps.location = Point(-0.066990,51.510020,srid=4326)
        ps.save()

        ps_qs = PollingStation.objects.filter(council_id='E09000011')
        for ps in ps_qs:
            ps.address = ps.address.replace('&rsquo;', "’")
            ps.save()

        try:
            ps = PollingStation.objects.get(
                postcode='N1 2PY', council_id='E09000019')
            ps.postcode = "N1 2SX"
            ps.location = Point(
                -0.090005,
                51.545168,
                srid=4326
            )
            ps.save()
        except PollingStation.DoesNotExist:
            pass

        ps = PollingStation.objects.get(
            internal_council_id='C', council_id='E09000021')
        ps.address = "Hook Centre, Hook Road"
        ps.postcode = "KT9 1EJ"
        ps.location = Point(
            -0.306091,
            51.368013,
            srid=4326
        )
        ps.save()

        ps = PollingStation.objects.get(
            internal_council_id='KB', council_id='E09000021')
        ps.address = "Malden Manor Children's centre, Lawrence Avenue"
        ps.postcode = "KT3 5PF"
        ps.location = Point(
            -0.262148,
            51.386151,
            srid=4326
        )
        ps.save()


        ps = PollingStation.objects.get(
            internal_council_id="BD16", council_id='E09000002')
        ps.address = "Erkenwald Tuition Centre, Marlborough Road"
        ps.postcode = "RM8 2HU"
        ps.location = Point(
            0.127899,
            51.536587,
            srid=4326
        )
        ps.save()



        ps = PollingStation.objects.get(
            council_id='E09000029', internal_council_id="EA")
        ps.location = Point(
            -0.196271,
            51.371643,
            srid=4326
        )
        ps.save()

        ps = PollingStation.objects.get(
            council_id='E09000030', internal_council_id="BS3")
        ps.location = Point(
            -0.012578,
            51.523169,
            srid=4326
        )
        ps.save()
