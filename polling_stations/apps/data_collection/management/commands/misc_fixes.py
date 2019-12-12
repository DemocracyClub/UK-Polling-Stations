from django.core.management.base import BaseCommand

from django.contrib.gis.geos import Point
from pollingstations.models import PollingStation, PollingDistrict, ResidentialAddress
from councils.models import Council
from addressbase.models import Address


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

        # https://trello.com/c/29TzIzEB
        print("updating: District PF (Calderdale)...")
        stations = PollingStation.objects.filter(
            council_id="E08000033", internal_council_id="PF"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = (
                "The Community Room\nHalifax Fire Station\nSkircoat Moor Road\nHalifax"
            )
            station.postcode = "HX1 3JF"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        # from the EC
        print("updating: District NL148 (North Lanarkshire)...")
        stations = PollingStation.objects.filter(
            council_id="S12000050", internal_council_id="NL148"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = "Knowetop Primary School\nKnowetop Avenue\nMotherwell"
            station.postcode = "ML1 2AG"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        # User issue 230
        print("updating: West Oxford Community Centre (Oxford)...")
        update_station_point(
            "E07000178", "5354", Point(-1.274921, 51.752621, srid=4326)
        )

        # User issue 237
        print("updating: ATHERSLEY COMMUNITY SHOP (Barnsley)...")
        update_station_point("E08000016", "45", Point(-1.479578, 53.583410, srid=4326))

        # User issue 238
        print("updating: YMCA - Lawnswood Branch (Leeds)...")
        update_station_point(
            "E08000035", "7664", Point(-1.595989, 53.844380, srid=4326)
        )

        # User issue 239
        print("updating: Merrion House (Leeds)...")
        stations = PollingStation.objects.filter(
            council_id="E08000035", internal_council_id="7387"
        )
        if len(stations) == 1:
            station = stations[0]
            station.postcode = "LS2 8PD"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        # Correction from Tunbridge Wells
        print("updating: District JJ (Tunbridge Wells)...")
        stations = PollingStation.objects.filter(
            council_id="E07000116", internal_council_id="JJ"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = "Pantiles Baptist Church, 73 Frant Road, Tunbridge Wells"
            station.postcode = "TN2 5LH"
            station.location = Point(558296, 137921, srid=27700)
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        # User issue 253
        print("updating: SOUTHFIELDS COMMUNITY CENTRE (Bedford)...")
        stations = PollingStation.objects.filter(
            council_id="E06000055",
            internal_council_id__in=["BAR_1", "BAR_2", "BAR_3", "BAR_4", "BAR_5"],
        )
        if len(stations) == 5:
            for station in stations:
                station.location = Point(-0.482075, 52.113823, srid=4326)
                station.save()
                print("..updated")
        else:
            print("..NOT updated")

        # User issue 261
        print("updating: West Ardsley Methodist Church (Leeds)...")
        update_station_point(
            "E08000035", "7800", Point(-1.5725806, 53.71417, srid=4326)
        )

        # User issue 272
        print("updating: Meadowbank Church of Scotland (Edinburgh)...")
        stations = PollingStation.objects.filter(
            council_id="S12000036", internal_council_id="EN12K"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = "Norton Park Conference Centre, 53 Albion Road"
            station.postcode = "EH7 5QY"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        # User issue 273
        print("updating: Maitland Park Gym (Camden)...")
        stations = PollingStation.objects.filter(
            council_id="E09000007", internal_council_id="LA"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = "Rhyl Primary School, 7-31 Rhyl Street, London"
            station.postcode = "NW5 3HB"
            station.location = Point(-0.150516, 51.547817, srid=4326)
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        # User issue 285
        print("updating: Memorial Hall (Middlesbrough)...")
        update_station_point(
            "E06000002", "8607", Point(-1.259325, 54.520594, srid=4326)
        )

        # User issue 288
        print("updating: Thame Snooker Club...")
        update_station_point(
            "E07000179", "8327", Point(-0.9743458, 51.7464972, srid=4326)
        )

        # User issue 290
        print("updating: Temporary at Wingfield Rd...")
        update_station_point("E08000016", "48", None)

        # User issue 314
        print("updating: Harrold Chapel...")
        update_station_point(
            "E06000055", "NW_1", Point(-0.613711, 52.202050, srid=4326)
        )

        # User issue 317
        print("updating: Aubert Court Community Centre...")
        update_station_point("E09000019", "1704", None)

        # User issue 323
        print("updating: Trust Hall-Stoke Gifford...")
        update_station_point(
            "E06000025", "11076", Point(-2.540850, 51.516671, srid=4326)
        )

        # User issue 333
        print("updating: Ince Independent Methodist Church...")
        update_station_point("E08000010", "6192", None)

        # User issue 339
        print("updating: ROYAL QUAYS COMMUNITY CENTRE...")
        update_station_point("E08000022", "FF", None)

        # User issue 346
        print("updating: BROUGHTON VILLAGE HALL...")
        update_station_point("S12000026", "01G", None)

        # User issue 347
        print("updating:  Newton Childrens Centre...")
        update_station_point("E08000013", "3741", None)

        # User issue 349
        print("updating:  Kingswood Play Area Hall...")
        update_station_point("E07000066", "4613", None)

        # User issue 351
        print("updating: BARNSLEY MBC SPRINGVALE DEPOT...")
        update_station_point("E08000016", "146", None)

        print("removing bad points from AddressBase")
        bad_uprns = [
            # nothing yet
        ]
        addresses = Address.objects.filter(pk__in=bad_uprns)
        for address in addresses:
            print(address.uprn)
            address.delete()
        print("..deleted")

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
