import json
from html import unescape

import requests
from councils.models import Council, CouncilGeography, UnsafeToDeleteCouncil
from django.apps import apps
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon, WKTWriter
from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS, transaction
from requests.exceptions import HTTPError
from retry import retry


from polling_stations.settings.constants.councils import (
    COUNCIL_ID_FIELD,
    NIR_IDS,
    WELSH_COUNCIL_NAMES,
)


def union_areas(a1, a2):
    if not a1:
        return a2
    return MultiPolygon(a1.union(a2))


# Sometimes we want to get most boundaries from one ONS file, but some from an older one.
# In 2024 this was because there were some new unitaries which had combined their electoral services teams, and some
# which still wanted to have separate contact details for the teams which mapped onto the old districts.
# This meant we added the gss codes for Westmoreland and Furness Council and Somerset Council to the `exclude` parameter
# in the call to self.attach_boundaries(). Then if the command was run with the lines in OLD_BOUNDARIES_GSS_CODES uncommented
# and the --import-old-boundaries flag, we would grab geoms for the old districts from OLD_BOUNDARY_URL.
# This also required that there was an entry for each of the old districts in the EC contact details, where the name field
# matched the new unitary (with a '(formerly ...)'), but the 'code', 'electoral_services' and 'identifiers' fields details
# matched the old districts.
OLD_BOUNDARY_URL = "https://s3.eu-west-2.amazonaws.com/pollingstations.public.data/ons/boundaries/Local_Authority_Districts_May_2022_UK_BFE_V3.geojson"
OLD_BOUNDARIES_GSS_CODES = [
    # "E07000187",  # MEN Mendip
    # "E07000188",  # SEG Sedgemoor
    # "E07000246",  # SWT Somerset West & Taunton
    # "E07000189",  # SSO South Somerset
    # "E07000031",  # SLA South Lakeland
    # "E07000030",  # EDN Eden
    # "E07000027",  # BAR Barrow
]
OLD_ID_FIELD = "LAD22CD"

# There have been problems getting accurate NI data from boundary line (2023).
# The values from these constants can be used to get the NI Boundaries from a different source. In this case OSNI.
# The command will need to be called with the '--use-osni' flag, but you could obviously put a different url in here.
# You will probably also need to add the NI_BOUNDARY_GSS_CODES list to the `exclude` parameter in the call to self.attach_boundaries()
NI_BOUNDARY_URL = "https://s3.eu-west-2.amazonaws.com/pollingstations.public.data/osni/OSNI_Open_Data_-_Largescale_Boundaries_-_Local_Government_Districts_2012.geojson"
NI_BOUNDARY_GSS_CODES = [
    "N09000001",  # ANN Antrim and Newtownabbey
    "N09000002",  # ABC Armagh City, Banbridge and Craigavon
    "N09000003",  # BFS Belfast
    "N09000004",  # CCG Causeway Coast and Glens
    "N09000005",  # DRS Derry City and Strabane
    "N09000006",  # FMO Fermanagh and Omagh
    "N09000007",  # LBC Lisburn and Castlereagh
    "N09000008",  # MEA Mid and East Antrim
    "N09000009",  # MUL Mid Ulster
    "N09000010",  # NMD Newry, Mourne and Down
    "N09000011",  # AND Ards and North Down
]
NI_ID_FIELD = "LGDCode"


class Command(BaseCommand):
    """
    Turn off auto system check for all apps
    We will maunally run system checks only for the
    'councils' and 'pollingstations' apps
    """

    requires_system_checks = []
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
            help="<Optional> Alternative url to override settings.https://s3.eu-west-2.amazonaws.com/pollingstations.public.data/ons/boundaries/Local_Authority_Districts_May_2023_UK_BFE_V2.geojson",
        )
        parser.add_argument(
            "--only-contact-details",
            action="store_true",
            help="Only update contact information for imported councils, "
            "don't update boundaries",
        )
        parser.add_argument(
            "--database",
            default=DEFAULT_DB_ALIAS,
            help='Nominates a database to import in to. Defaults to the "default" database.',
        )
        parser.add_argument(
            "--import-old-boundaries",
            required=False,
            action="store_true",
            default=False,
            help="<Optional> Import the old boundaries",
        )
        parser.add_argument(
            "--use-osni",
            required=False,
            action="store_true",
            default=False,
            help="<Optional> Import the NI boundaries from OSNI",
        )

    def feature_to_multipolygon(self, feature):
        geometry = GEOSGeometry(json.dumps(feature["geometry"]), srid=4326)
        if geometry.hasz:
            wkt_w = WKTWriter()
            wkt_w.outdim = 2
            temp_wkt = wkt_w.write(geometry)
            geometry = GEOSGeometry(temp_wkt)
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

    def attach_boundaries(
        self, url=None, id_field=COUNCIL_ID_FIELD, include=None, exclude=None
    ):
        """
        Fetch each council's boundary from geojson at 'url' and attach it to an existing
        council object

        :param url: The URL of the geoJSON file containing council boundaries
        :param id_field: The name of the feature properties field containing
                         the council GSS code
        :param include: A list of codes to get boundaries for. If None then attempt all.
        :param exclude: A list of codes not to attempt to get boundaries for. If None then attempt all.
        :return:
        """
        if not url:
            url = settings.BOUNDARIES_URL
        self.stdout.write("Downloading boundaries from %s..." % (url))
        feature_collection = self.get_ons_boundary_json(url)
        for feature in feature_collection["features"]:
            gss_code = feature["properties"][id_field]
            if include and gss_code not in include:
                continue
            if exclude and gss_code in exclude:
                continue
            try:
                council = Council.objects.using(self.database).get(
                    identifiers__contains=[gss_code]
                )
                self.stdout.write(
                    "Found boundary for %s: %s" % (gss_code, council.name)
                )
            except Council.DoesNotExist:
                self.stderr.write(
                    "No council object with GSS {} found".format(gss_code)
                )
                continue

            self.attach_council_geography(council, feature, gss_code)

    def attach_council_geography(self, council: Council, feature: dict, gss_code: str):
        try:
            council_geography = CouncilGeography.objects.using(self.database).get(
                council=council
            )
        except CouncilGeography.DoesNotExist:
            council_geography = CouncilGeography(council=council)

        council_geography.gss = gss_code
        council_geography.geography = self.feature_to_multipolygon(feature)
        council_geography.save(using=self.database)

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
            if council_data["code"] in self.seen_ids:
                continue

            self.seen_ids.add(council_data["code"])

            try:
                council = Council.objects.using(self.database).get(
                    council_id=council_data["code"]
                )
            except Council.DoesNotExist:
                council = Council(council_id=council_data["code"])

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

            if council.council_id in WELSH_COUNCIL_NAMES:
                council.name_translated["cy"] = WELSH_COUNCIL_NAMES[council.council_id]
            elif council.name_translated.get("cy"):
                del council.name_translated["cy"]

            council.save(using=self.database)

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

        self.database = options["database"]

        with transaction.atomic(self.database):
            if options["teardown"]:
                try:
                    self.stdout.write("Clearing councils table..")
                    Council.objects.using(self.database).all().delete()
                    self.stdout.write("Clearing councils_geography table..")
                    CouncilGeography.objects.using(self.database).all().delete()
                except UnsafeToDeleteCouncil:
                    self.stdout.write(
                        "Can't delete councils there are polling stations attached. "
                        "Please run manage.py teardown --all first if you want to delete them."
                    )
                    return

            self.seen_ids = set()
            self.import_councils_from_ec()

            if not options["only_contact_details"]:
                self.attach_boundaries(options.get("alt_url"))

                if options.get("use_osni", None):
                    self.attach_boundaries(
                        NI_BOUNDARY_URL,
                        id_field=NI_ID_FIELD,
                        include=NI_BOUNDARY_GSS_CODES,
                    )

                if options.get("import_old_boundaries", None):
                    self.attach_boundaries(
                        OLD_BOUNDARY_URL,
                        id_field=OLD_ID_FIELD,
                        include=OLD_BOUNDARIES_GSS_CODES,
                    )

            # Clean up old councils that we've not seen in the EC data
            Council.objects.using(self.database).exclude(
                council_id__in=self.seen_ids
            ).delete()

            self.stdout.write("..done")
