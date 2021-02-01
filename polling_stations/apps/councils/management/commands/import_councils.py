import json
from html import unescape

import requests
from django.apps import apps
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon
from django.conf import settings
from django.core.management.base import BaseCommand
from requests.exceptions import HTTPError
from retry import retry
from councils.models import Council, CouncilGeography


def union_areas(a1, a2):
    if not a1:
        return a2
    return MultiPolygon(a1.union(a2))


NIR_IDS = [
    "ABC",
    "AND",
    "ANN",
    "BFS",
    "CCG",
    "DRS",
    "FMO",
    "LBC",
    "MEA",
    "MUL",
    "NMD",
]


class Command(BaseCommand):
    """
    Turn off auto system check for all apps
    We will maunally run system checks only for the
    'councils' and 'pollingstations' apps
    """

    requires_system_checks = False
    contact_details = {}

    def add_arguments(self, parser):
        parser.add_argument(
            "-t",
            "--teardown",
            default=False,
            action="store_true",
            required=False,
            help="<Optional> Clear Councils and CouncilGeography tables before importing",
        )
        parser.add_argument(
            "-u",
            "--alt-url",
            required=False,
            help="<Optional> Alternative url to override settings.BOUNDARIES_URL",
        )
        parser.add_argument(
            "--only-contact-details",
            action="store_true",
            help="Only update contact information for imported councils, "
            "don't update boundaries",
        )

    def feature_to_multipolygon(self, feature):
        geometry = GEOSGeometry(json.dumps(feature["geometry"]), srid=4326)
        if isinstance(geometry, Polygon):
            return MultiPolygon(geometry)
        return geometry

    @retry(HTTPError, tries=2, delay=30)
    def get_ons_boundary_json(self, url):
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

    def attach_boundaries(self, url=None, id_field="lad19cd"):
        """
        Fetch each council's boundary from ONS and attach it to an existing
        council object

        :param url: The URL of the geoJSON file containing council boundaries
        :param id_field: The name of the feature properties field containing
                         the council ID
        :return:
        """
        if not url:
            url = settings.BOUNDARIES_URL
        self.stdout.write("Downloading ONS boundaries from %s..." % (url))
        feature_collection = self.get_ons_boundary_json(url)
        for feature in feature_collection["features"]:
            gss_code = feature["properties"][id_field]
            try:
                council = Council.objects.get(identifiers__contains=[gss_code])
                self.stdout.write(
                    "Found boundary for %s: %s" % (gss_code, council.name)
                )
            except Council.DoesNotExist:
                self.stderr.write(
                    "No council object with GSS {} found".format(gss_code)
                )
                continue

            council_geography, _ = CouncilGeography.objects.get_or_create(
                council=council
            )
            council_geography.gss = gss_code
            council_geography.geography = self.feature_to_multipolygon(feature)
            council_geography.save()

    def load_contact_details(self):
        return requests.get(settings.EC_COUNCIL_CONTACT_DETAILS_API_URL).json()

    def get_council_name(self, council_data):
        """
        At the time of writing, the council name can be NULL in the API
        meaning we can't rely on the key being populated in all cases.

        This is normally only an issue with councils covered by EONI, so if
        we see one of them without a name, we assign a hardcoded name.

        """
        name = None
        if council_data["official_name"]:
            name = council_data["official_name"]
        else:
            if council_data["code"] in NIR_IDS:
                name = "Electoral Office for Northern Ireland"
        if not name:
            raise ValueError("No official name for {}".format(council_data["code"]))
        return unescape(name)

    def import_councils_from_ec(self):
        self.stdout.write("Importing councils...")

        for council_data in self.load_contact_details():
            self.seen_ids.add(council_data["code"])
            council, _ = Council.objects.get_or_create(council_id=council_data["code"])

            council.name = self.get_council_name(council_data)
            council.identifiers = council_data["identifiers"]

            if council_data["electoral_services"]:
                electoral_services = council_data["electoral_services"][0]
                council.electoral_services_email = electoral_services["email"]
                council.electoral_services_address = unescape(
                    electoral_services["address"]
                )
                council.electoral_services_postcode = electoral_services["postcode"]
                council.electoral_services_phone_numbers = electoral_services["tel"]
                council.electoral_services_website = electoral_services[
                    "website"
                ].replace("\\", "")
            if council_data["registration"]:
                registration = council_data["registration"][0]
                council.registration_email = registration["email"]
                council.registration_address = unescape(registration["address"])
                council.registration_postcode = registration["postcode"]
                council.registration_phone_numbers = registration["tel"]
                council.registration_website = registration["website"].replace("\\", "")

            council.save()

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
            self.stdout.write("Clearing councils_geography table..")
            CouncilGeography.objects.all().delete()

        self.seen_ids = set()
        self.import_councils_from_ec()

        if not options["only_contact_details"]:
            self.attach_boundaries(options.get("alt_url"))

        # Clean up old councils that we've not seen in the EC data
        Council.objects.exclude(council_id__in=self.seen_ids).delete()

        self.stdout.write("..done")
