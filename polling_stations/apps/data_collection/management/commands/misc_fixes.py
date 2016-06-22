from django.core.management.base import BaseCommand

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
