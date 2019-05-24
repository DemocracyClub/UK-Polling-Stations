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

        print("updating Watford address...")
        watford = Council.objects.get(pk="E07000103")
        watford.address = "Electoral Services Office\nRoom 22\nTown Hall\nWatford"
        watford.postcode = "WD17 3EX"
        watford.save()
        print("..updated")

        print("updating Harrogate address...")
        harrogate = Council.objects.get(pk="E07000165")
        harrogate.address = "Civic Centre\nSt Lukes Avenue\nHarrogate"
        harrogate.postcode = "HG1 2AE"
        harrogate.save()
        print("..updated")

        print("updating Oadby & Wigston name...")
        oadby = Council.objects.get(pk="E07000135")
        oadby.name = "Oadby & Wigston Borough Council"
        oadby.save()
        print("..updated")

        print("updating Swansea name...")
        swansea = Council.objects.get(pk="W06000011")
        swansea.name = "City & County of Swansea"
        swansea.save()
        print("..updated")

        print("updating Wyre Forest phone number")
        wyre_forest = Council.objects.get(pk="E07000239")
        wyre_forest.phone = "01562 732928 / 01562 732733"
        wyre_forest.save()
        print("..updated")

        print("updating Chelmsford phone number")
        chelmsford = Council.objects.get(pk="E07000070")
        chelmsford.phone = "01245 606449"
        chelmsford.save()
        print("..updated")

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
