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

        # User issue 149
        print("updating: The Mount View Hotel...")
        update_station_point(
            "E06000052", "3241", Point(-5.499815, 50.129318, srid=4326)
        )

        # User issue 139
        print("updating:  LARGS ACADEMY,...")
        stations = PollingStation.objects.filter(
            council_id="S12000021", internal_council_id="N804"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = "Largs Campus Gymnasium\nAlexander Avenue\nLargs"
            station.postcode = "KA30 9EU"
            station.location = Point(-4.855903, 55.8003773, srid=4326)
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        # User issue 151
        print("updating: Holy Trinity Church Hall...")
        update_station_point(
            "E07000081", "2657", Point(-2.2127903, 51.8753716, srid=4326)
        )

        # User issue 153
        print("updating: NETHERWITTON VILLAGE HALL...")
        update_station_point(
            "E06000057", "B37HAR", Point(-1.845624, 55.206558, srid=4326)
        )
        update_station_point(
            "E06000057", "B39MEL", Point(-1.845624, 55.206558, srid=4326)
        )
        update_station_point(
            "E06000057", "B41NET", Point(-1.845624, 55.206558, srid=4326)
        )

        # User issue 154/5
        print("updating:  Bolton Road United Reformed Church...")
        update_station_point(
            "E06000008", "3077", Point(-2.4615102, 53.6832739, srid=4326)
        )

        # User issue 157
        print("updating:  County Children`s Centre...")
        update_station_point(
            "E08000012", "5909", Point(-2.968792, 53.442462, srid=4326)
        )

        # User issue 158
        print("updating:  Caythorpe and Frieston Village Hall...")
        update_station_point("E07000141", "4056", Point(-0.60214, 53.02241, srid=4326))

        # Lambeth Council update / User issue 156
        print("updating: Raleigh Park Centre...")
        stations = PollingStation.objects.filter(
            council_id="E09000022", internal_council_id="SOB"
        )
        if len(stations) == 1:
            station = stations[0]
            station.location = Point(-0.1134, 51.452, srid=4326)
            station.address = "Jubilee Primary School & Children`s Centre\nTulse Hill"
            station.postcode = "SW2 2JE"
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        # User issue 162
        print("updating:  Newport Pagnell Town Footbal Club...")
        update_station_point(
            "E06000042", "7370", Point(-0.721871, 52.077798, srid=4326)
        )

        # User issue 163
        print("updating: Walkley Parish Community Hall...")
        stations = PollingStation.objects.filter(
            council_id="E08000019",
            internal_council_id="194-walkley-parish-community-hall",
        )
        if len(stations) == 1:
            station = stations[0]
            station.location = Point(-1.49913, 53.39145, srid=4326)
            station.address = " St. Mary’s Walkley Community Hall\nWalkley"
            station.postcode = ""
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        # User issue 167
        print("updating: Walkley Library...")
        update_station_point(
            "E08000019", "198-walkley-library", Point(-1.502873, 53.394934, srid=4326)
        )

        # Fife
        print("updating: Fife...")
        print("Updating: 027BAH")
        stations = PollingStation.objects.filter(
            council_id="S12000047", internal_council_id="027BAH"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = "Carnegie Primary School\nPittsburgh Road\nDunfermline"
            station.postcode = "KY11 8SS"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        print("Updating: 043CAD")
        stations = PollingStation.objects.filter(
            council_id="S12000047", internal_council_id="043CAD"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = (
                "Education Resource & Training Centre\nMaitland Street\nDunfermline "
            )
            station.postcode = "KY12 8AF"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        print("Updating: 045CAF")
        stations = PollingStation.objects.filter(
            council_id="S12000047", internal_council_id="045CAF"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = (
                "Touch Community Leisure Centre\n30 Mercer Place\nDunfermline "
            )
            station.postcode = "KY11 4UG"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        print("Updating: 046CAG")
        stations = PollingStation.objects.filter(
            council_id="S12000047", internal_council_id="046CAG"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = "Carnegie Primary School\nPittsburgh Road\nDunfermline"
            station.postcode = "KY11 8SS"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        print("Updating: 106GAB")
        stations = PollingStation.objects.filter(
            council_id="S12000047", internal_council_id="106GAB"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = (
                "Hill of Beath Ex-Servicemen’s Club\nMain Street\nHill of Beath"
            )
            station.postcode = "KY4 8DP"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        print("Updating: 112GAF")
        stations = PollingStation.objects.filter(
            council_id="S12000047", internal_council_id="112GAF"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = (
                "Maxwell Community Centre\n70 Stenhouse Street\nCowdenbeath"
            )
            station.postcode = "KY4 9DD"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        print("Updating: 112GAH")
        stations = PollingStation.objects.filter(
            council_id="S12000047", internal_council_id="112GAH"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = (
                "Maxwell Community Centre\n70 Stenhouse Street\nCowdenbeath"
            )
            station.postcode = "KY4 9DD"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        print("Updating: 201IAA")
        stations = PollingStation.objects.filter(
            council_id="S12000047", internal_council_id="201IAA"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = "Solid Rock Café\n245 High Street\nBurntisland "
            station.postcode = "KY3 9AQ"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        print("Updating: 211JAB")
        stations = PollingStation.objects.filter(
            council_id="S12000047", internal_council_id="211JAB"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = "Torbain Parish Church Hall\nCarron Place\nKirkcaldy"
            station.postcode = "KY2 6PS"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        print("Updating: 259NAE")
        stations = PollingStation.objects.filter(
            council_id="S12000047", internal_council_id="259NAE"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = (
                "The Nairn Suite\nBalgeddie House Hotel,Balgeddie Way\nGlenrothes"
            )
            station.postcode = "KY6 3ET"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        print("Updating: 307PAG")
        stations = PollingStation.objects.filter(
            council_id="S12000047", internal_council_id="307PAG"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = "Ladybank (Howe of Fife Parish) Church Hall\noff Church Street\nLadybank "
            station.postcode = "KY15 7ND"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        print("Updating: 325QAF")
        stations = PollingStation.objects.filter(
            council_id="S12000047", internal_council_id="325QAF"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = "Leuchars Primary School\n18 Pitlethie Road\nLeuchars"
            station.postcode = "KY16 0EZ"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")

        print("Updating: 373UAF")
        stations = PollingStation.objects.filter(
            council_id="S12000047", internal_council_id="373UAF"
        )
        if len(stations) == 1:
            station = stations[0]
            station.address = "Sports Pavilion\nCotlands Park\nKennoway "
            station.postcode = "KY8 5HX"
            station.location = None
            station.save()
            print("..updated")
        else:
            print("..NOT updated")
        print("...updated Fife")

        print("Updating: Perth & Kinross: SLI, SLL, SLM, SLN")
        stations = PollingStation.objects.filter(
            council_id="S12000048", internal_council_id__in=["SLI", "SLL", "SLM", "SLN"]
        )
        if len(stations) == 4:
            for station in stations:
                station.address = (
                    "Aytoun Hall, 91-93 High Street, Auchterarder, Perthshire"
                )
                station.postcode = ""
                station.location = None
                station.save()
                print("..updated")
        else:
            print("..NOT updated")

        # User issue 168
        print("updating: Kingswood Community Centre...")
        update_station_point("E06000007", "55", Point(-2.641653, 53.413628, srid=4326))

        # 2x Last-minute changes from Kingston council
        print("updating: Kingston-upon-Thames EA...")
        stations = PollingStation.objects.filter(
            council_id="E09000021", internal_council_id__in=["EA_25", "EA_26"]
        )
        if len(stations) == 2:
            for station in stations:
                station.address = "St. Mark's Church\nSt. Mark's Hill\nSurbiton"
                station.postcode = "KT6 4LS"
                station.location = Point(
                    -0.300536430202766, 51.3952050795307, srid=4326
                )
                station.save()
                print("..updated")
        else:
            print("..NOT updated")

        print("updating: Kingston-upon-Thames EB...")
        stations = PollingStation.objects.filter(
            council_id="E09000021", internal_council_id__in=["EB_27", "EB_28"]
        )
        if len(stations) == 2:
            for station in stations:
                station.address = "Glenmore House\n6 The Crescent\nSurbiton"
                station.postcode = "KT6 4BN"
                station.location = Point(
                    -0.305167559373057, 51.3951372632609, srid=4326
                )
                station.save()
                print("..updated")
        else:
            print("..NOT updated")

        #  Dorset via email https://trello.com/c/ZutXcLv1
        print("updating: East Chaldon Village Hall...")
        update_station_point(
            "E06000059", "31943", Point(-2.298479, 50.647704, srid=4326)
        )

        #  Denbigshire https://trello.com/c/GVoeeqnF
        print("updating: Canolfan Cymuned Ffordd Las Community Centre...")
        update_station_point(
            "W06000004", "8156", Point(-3.488767, 53.315241, srid=4326)
        )

        # User issue #171
        print("updating: Brooklands Pavilion...")
        update_station_point("E06000042", "7297", Point(-0.67579, 52.04455, srid=4326))

        # User issue #170
        print("updating: The Oval Primary School...")
        update_station_point(
            "E08000025",
            "139-the-oval-primary-school",
            Point(-1.79646, 52.47996, srid=4326),
        )
