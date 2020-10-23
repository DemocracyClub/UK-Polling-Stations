from django.core.management.base import BaseCommand

# from django.contrib.gis.geos import Point
from pollingstations.models import PollingStation, PollingDistrict
from councils.models import Council
from addressbase.models import Address, UprnToCouncil


def update_station_point(council_id, station_id, point):
    stations = PollingStation.objects.filter(
        council_id=council_id, internal_council_id=station_id
    )
    if len(stations) == 1:
        station = stations[0]
        station.location = point
        station.save()
        print("..updated")
    else:
        print("..NOT updated")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        print("removing bad points from AddressBase")
        bad_uprns = [
            # nothing yet
        ]
        addresses = Address.objects.filter(pk__in=bad_uprns)
        for address in addresses:
            print(address.uprn)
            address.delete()
        print("..deleted")
        print("removing bad uprns from uprn lookup")
        uprns = UprnToCouncil.objects.filter(pk__in=bad_uprns)
        for uprn in uprns:
            print(uprn.pk)
            uprn.delete()
        print(".. deleted")

        deleteme = [
            # nothing yet
        ]
        for council_id in deleteme:
            print("Deleting data for council %s..." % (council_id))
            # check this council exists
            c = Council.objects.get(pk=council_id)
            print(c.name)

            PollingStation.objects.filter(council=council_id).delete()
            PollingDistrict.objects.filter(council=council_id).delete()
            UprnToCouncil.objects.filter(lad=council_id).update(polling_station_id="")
            print("..deleted")

        print("..done")
