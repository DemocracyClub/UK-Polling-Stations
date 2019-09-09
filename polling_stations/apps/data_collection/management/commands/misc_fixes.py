from django.core.management.base import BaseCommand

# from django.contrib.gis.geos import Point
from pollingstations.models import PollingStation, PollingDistrict, ResidentialAddress
from councils.models import Council
from addressbase.models import Address, Blacklist


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

        print("removing dodgy blacklist entries (result of bad point in AddressBase)..")
        blacklist = Blacklist.objects.filter(postcode="RH122LP")
        if len(blacklist) == 2:
            for b in blacklist:
                b.delete()
                print("..deleted")
        else:
            print("..NOT deleted")

        print(
            "removing dodgy blacklist entries (result of bad points in AddressBase).."
        )
        blacklist = Blacklist.objects.filter(postcode="S24AX")
        if len(blacklist) == 2:
            for b in blacklist:
                b.delete()
                print("..deleted")
        else:
            print("..NOT deleted")

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
            ResidentialAddress.objects.filter(council=council_id).delete()
            print("..deleted")

        print("..done")
