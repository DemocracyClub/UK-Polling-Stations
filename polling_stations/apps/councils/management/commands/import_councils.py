import html
import json
from json.decoder import JSONDecodeError
import requests
from django.apps import apps
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon
from django.conf import settings
from django.core.management.base import BaseCommand
from requests.exceptions import HTTPError
from retry import retry
from councils.models import Council


def union_areas(a1, a2):
    if not a1:
        return a2
    return MultiPolygon(a1.union(a2))


TEMP_CONTACT_DETAILS = {
    "E07000246": {
        "name": "Somerset West & Taunton Council",
        "website": "https://www.somersetwestandtaunton.gov.uk/",
        "email": "elections@somersetwestandtaunton.gov.uk",
        "phone": "01823 358692",
        "address": "Electoral Services\nWest Somerset House\nKillick Way\nWilliton",
        "postcode": "TA4 4QA",
    },
    "E06000058": {
        "name": "Bournemouth, Christchurch & Poole Council",
        "website": "https://www.bcpcouncil.gov.uk",
        "email": "elections@bcpcouncil.gov.uk",
        "phone": "01202 633097",
        "address": "Town Hall\nBourne Avenue\nBournemouth",
        "postcode": "BH2 6DY",
    },
    "E06000059": {
        "name": "Dorset Council",
        "website": "https://www.dorset.gov.uk/",
        "email": "elections@dorset.gov.uk",
        "phone": "01305 838299",
        "address": "South Walks House\nSouth Walks Road\nDorchester",
        "postcode": "DT1 1UZ",
    },
    "E07000244": {
        "name": "East Suffolk Council",
        "website": "https://www.eastsuffolk.gov.uk/",
        "email": "elections@eastsuffolk.gov.uk",
        "phone": "01394 444422",
        "address": "East Suffolk House\nStation Road\nMelton\nWoodbridge",
        "postcode": "IP12 1RT",
    },
    "E07000245": {
        "name": "West Suffolk Council",
        "website": "https://www.westsuffolk.gov.uk/",
        "email": "elections@westsuffolk.gov.uk",
        "phone": "01284 757131",
        "address": "Suffolk House\nWestern Way\nBury St Edmunds\nSuffolk",
        "postcode": "IP33 3YU",
    },
}


class Command(BaseCommand):
    """
    Turn off auto system check for all apps
    We will maunally run system checks only for the
    'councils' and 'pollingstations' apps
    """

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            "-t",
            "--teardown",
            default=False,
            action="store_true",
            required=False,
            help="<Optional> Clear Councils table before importing",
        )
        parser.add_argument(
            "-u",
            "--alt-url",
            required=False,
            help="<Optional> Alternative url to override settings.BOUNDARIES_URL",
        )

    def feature_to_multipolygon(self, feature):
        geometry = GEOSGeometry(json.dumps(feature["geometry"]), srid=4326)
        if isinstance(geometry, Polygon):
            return MultiPolygon(geometry)
        return geometry

    @retry(HTTPError, tries=2, delay=30)
    def get_json(self, url):
        r = requests.get(url)
        r.raise_for_status()
        """
        When an ArcGIS server can't generate a response
        within X amount of time, it will return a 202 ACCEPTED
        response with a body like
        {
            "processingTime": "27.018 seconds",
            "status": "Processing",
            "generating": {}
        }
        and expects the client to poll it.
        """
        if r.status_code == 202:
            raise HTTPError("202 Accepted", response=r)
        return r.json()

    def get_councils(self, url, id_field, name_field):
        # call url and return a list of Council objects
        # with the code and boundary fields populated
        # (ready to atttach contact details to)
        councils = []
        feature_collection = self.get_json(url)
        for feature in feature_collection["features"]:
            council_id = feature["properties"][id_field]
            self.stdout.write(
                "Found boundary for %s: %s"
                % (council_id, feature["properties"][name_field])
            )
            poly = self.feature_to_multipolygon(feature)
            councils.append(Council(council_id=council_id, area=poly))
        return councils

    def pre_process_councils(self, councils):
        """
        if the new councils for 2019 don't already
        exist in the input file we need to:
        - build the boundaries as a union of
          the old authorities that they replace
        - delete the old ones out of the councils array so
          we don't have >1 polygons covering the same area
        """

        new_council_objects = {}
        for code in settings.NEW_COUNCILS:
            # only attempt to build the new areas if they don't already exist
            if code not in [c.council_id for c in councils]:
                new_council_objects[code] = Council(council_id=code, area=None)

        self.stdout.write(
            "building new areas: {}".format(str(list(new_council_objects.keys())))
        )

        # ids of any councils we're going to delete
        deleteme = []

        for council in councils:
            if not council.council_id in settings.OLD_TO_NEW_MAP:
                continue
            code = settings.OLD_TO_NEW_MAP[council.council_id]
            if code in new_council_objects:
                new_council_objects[code].area = union_areas(
                    new_council_objects[code].area, council.area
                )
                self.stdout.write("{} --> {}".format(council.council_id, code))
                deleteme.append(council.council_id)

        councils = [c for c in councils if c.council_id not in deleteme]

        for code, council in new_council_objects.items():
            councils.append(council)

        return councils

    def clean_url(self, url):
        if not url.startswith(("http://", "https://")):
            # Assume http everywhere will redirect to https if it is there.
            url = "http://{}".format(url)
        return url

    def get_from_yvm(self, council_id):
        url = "{}{}".format(settings.YVM_LA_URL, council_id)
        req = requests.get(url)
        return req.json()

    def get_contact_info_from_yvm(self, council_id):
        try:
            data = self.get_from_yvm(council_id)
        except JSONDecodeError as e:
            # YNM returns a 200 OK with HTML body if code not found
            # If YVM isn't using the new codes yet, use the old codes
            # to fetch the electoral services contact info
            if council_id == "S12000047":
                # Fife
                data = self.get_from_yvm("S12000015")
            elif council_id == "S12000048":
                # Perth & Kinross
                data = self.get_from_yvm("S12000024")
            elif council_id in TEMP_CONTACT_DETAILS:
                self.stdout.write("No contact details available from YVM")
                return TEMP_CONTACT_DETAILS[council_id]
            else:
                raise e

        council_data = data["registrationOffice"]
        info = {}
        info["name"] = html.unescape(council_data.get("office"))
        info["website"] = self.clean_url(council_data.get("website"))
        info["email"] = council_data.get("email").strip()
        info["phone"] = (
            council_data.get("telephone", "").replace("</a>", "").split(">")[-1]
        )

        address_fields = [
            council_data.get(f, "")
            for f in ["address1", "address2", "address3", "city", "address4"]
        ]
        info["address"] = "\n".join([f for f in address_fields if f])
        info["postcode"] = " ".join(council_data.get("postalcode", "").split(" ")[-2:])

        return info

    def handle(self, **options):
        """
        Manually run system checks for the
        'councils' and 'pollingstations' apps
        Management commands can ignore checks that only apply to
        the apps supporting the website part of the project
        """
        self.check(
            [apps.get_app_config("councils"), apps.get_app_config("pollingstations")]
        )

        if options["teardown"]:
            self.stdout.write("Clearing councils table..")
            Council.objects.all().delete()

        boundaries_url = settings.BOUNDARIES_URL
        if options["alt_url"]:
            boundaries_url = options["alt_url"]

        councils = []
        self.stdout.write("Downloading ONS boundaries from %s..." % (boundaries_url))
        councils = councils + self.get_councils(
            boundaries_url, id_field="lad19cd", name_field="lad19nm"
        )

        councils = self.pre_process_councils(councils)

        for council in councils:
            self.stdout.write(
                "Getting contact info for %s from YourVoteMatters"
                % (council.council_id)
            )

            info = self.get_contact_info_from_yvm(council.council_id)
            council.name = info["name"]
            council.website = info["website"]
            council.email = info["email"]
            council.phone = info["phone"]
            council.address = info["address"]
            council.postcode = info["postcode"]

            council.save()

        self.stdout.write("..done")
