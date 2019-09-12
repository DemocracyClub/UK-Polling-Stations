import csv
from collections import namedtuple
import json
import os
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
            help="<Optional> Clear Councils table before importing",
        )
        parser.add_argument(
            "-u",
            "--alt-url",
            required=False,
            help="<Optional> Alternative url to override settings.BOUNDARIES_URL",
        )
        parser.add_argument(
            "--contact-type",
            dest="contact_type",
            action="store",
            required=False,
            choices=("vjbs", "councils"),
            default="vjbs",
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

    def load_contact_details(self, contact_type):
        files = [
            "./polling_stations/apps/councils/data/england-wales.csv",
            "./polling_stations/apps/councils/data/ni.csv",
        ]

        if contact_type == "vjbs":
            files.append("./polling_stations/apps/councils/data/scotland-vjbs.csv")
        if contact_type == "councils":
            files.append("./polling_stations/apps/councils/data/scotland-councils.csv")

        for filename in files:
            with open(os.path.abspath(filename)) as infile:
                reader = csv.reader(infile)
                Row = namedtuple("Row", next(reader))
                for row in map(Row._make, reader):
                    self.contact_details[row.gss] = row

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

        self.stdout.write("Attaching contact details...")
        self.load_contact_details(options["contact_type"])
        for council in councils:
            contact_details = self.contact_details[council.council_id]
            council.name = contact_details.name
            council.website = contact_details.website
            council.email = contact_details.email
            council.phone = contact_details.phone
            council.address = contact_details.address
            council.postcode = contact_details.postcode

            council.save()

        self.stdout.write("..done")
