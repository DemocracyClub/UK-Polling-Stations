from django.core.management.base import BaseCommand

from django.contrib.gis.geos import Point
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
            "10023906550",
            "2630153843",
            "14059977",
            "10007921239",
            "10007920387",
            "10007920390",
            "10024288188",
            "10024288190",
            "10024288189",
            "10023117526",
            "10009922833",
            "10014047099",
            "28033460",
            "200004338783",
            "117134558",
            "138055880",
            "120036643",
            "120033242",
            "120033702",
            "120024279",
            "120047832",
            "120034278",
            "118191899",
            "118192006",
            "118190963",
            "118052842",
            "118126542",
            "118174746",
            "130075135",
            "130075151",
            "10091827317",
            "130142788",
            "130009944",
            "130137997",
            "130111463",
            "130038545",
            "130084948",
            "130059878",
            "130074399",
            "130074400",
            "130093312",
            "130148126",
            "130086434",
            "130148125",
            "130074398",
            "130105180",
            "130103488",
            "130127660",
            "130167898",
            "130077044",
            "130167897",
            "130077043",
            "130167902",
            "130148803",
            "130164482",
            "130088352",
            "130137432",
            "130168686",
            "130119378",
            "130148651",
            "130109313",
            "130145384",
            "130128377",
            "130144376",
            "130140027",
            "130144375",
            "130126560",
            "130144377",
            "130128375",
            "130128378",
            "130148146",
            "130113711",
            "130133033",
            "130128376",
            "130145383",
            "130113709",
            "130085106",
            "130116030",
            "130102440",
            "130136303",
            "130058258",
            "130058257",
            "130125391",
            "130166645",
            "130138981",
            "130168221",
            "130085141",
            "130099734",
            "130099735",
            "130136306",
            "130058259",
            "130151706",
            "130092504",
            "10091804094",
            "130058260",
            "130136304",
            "130136305",
            "130060270",
            "130180034",
            "130060273",
            "130168645",
            "130060274",
            "130060271",
            "130083808",
            "130060272",
            "130060275",
            "130168589",
            "130060268",
            "130061433",
            "130063761",
            "130147945",
            "130103286",
            "130104545",
            "130127885",
            "130103285",
            "130103287",
            "130075028",
            "130083586",
            "130149747",
            "130136566",
            "130086506",
            "130118347",
            "130143875",
            "130085874",
            "130066045",
            "130117060",
            "130135866",
            "130177987",
            "130073907",
            "130073905",
            "130073906",
            "130099688",
            "151651178",
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

        # User issue 140
        print("updating: Kilsby Village Hall (Kilsby Room)...")
        update_station_point(
            "E07000151", "6718", Point(-1.174253, 52.336931, srid=4326)
        )

        # User issue 141
        print("updating:  The Albert Underwood Room, St Peters Church...")
        stations = PollingStation.objects.filter(
            council_id="E07000152", internal_council_id="8545"
        )
        if len(stations) == 1:
            station = stations[0]
            station.postcode = "NN9 5WB"
            station.location = Point(-0.61056, 52.32575, srid=4326)
            station.save()
            print("..updated")
        else:
            print("..NOT updated")
