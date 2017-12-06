import html
import json
import requests
from django.apps import apps
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon
from django.conf import settings
from django.core.management.base import BaseCommand
from councils.models import Council


class Command(BaseCommand):
    """
    Turn off auto system check for all apps
    We will maunally run system checks only for the
    'councils' and 'pollingstations' apps
    """
    requires_system_checks = False


    def add_arguments(self, parser):
        parser.add_argument(
            '-t',
            '--teardown',
            default=False,
            action='store_true',
            required=False,
            help="<Optional> Clear Councils table before importing"
        )
        parser.add_argument(
            '-u',
            '--alt-url',
            required=False,
            help='<Optional> Alternative url to override settings.BOUNDARIES_URL',
        )


    def feature_to_multipolygon(self, feature):
        geometry = GEOSGeometry(json.dumps(feature['geometry']), srid=4326)
        if isinstance(geometry, Polygon):
            return MultiPolygon(geometry)
        return geometry

    def get_json(self, url):
        r = requests.get(url)
        r.raise_for_status()
        return r.json()

    def get_councils(self, url, id_field, name_field):
        # call url and return a list of Council objects
        # with the code and boundary fields populated
        # (ready to atttach contact details to)
        councils = []
        feature_collection = self.get_json(url)
        for feature in feature_collection['features']:
            council_id = feature['properties'][id_field]
            self.stdout.write("Found boundary for %s: %s" % (council_id, feature['properties'][name_field]))
            poly = self.feature_to_multipolygon(feature)
            councils.append(Council(council_id=council_id, area=poly))
        return councils

    def _save_council(self, council):
        # write council object to ALL databases
        for db in settings.DATABASES.keys():
            council.save(using=db)

    def clean_url(self, url):
        if not url.startswith(('http://', 'https://')):
            # Assume http everywhere will redirect to https if it is there.
            url = "http://{}".format(url)
        return url

    def get_contact_info_from_yvm(self, council_id):
        url = "{}{}".format(settings.YVM_LA_URL, council_id)

        req = requests.get(url)
        content = req.text

        council_data = json.loads(str(content))['registrationOffice']
        info = {}
        info['name'] = html.unescape(council_data.get('office'))
        info['website'] = self.clean_url(council_data.get('website'))
        info['email'] = council_data.get('email')
        info['phone'] = council_data.get('telephone', '').replace('</a>', '')\
            .split('>')[-1]

        address_fields = [council_data.get(f, '') for f in [
           'address1',
           'address2',
           'address3',
           'city',
           'address4',

        ]]
        info['address'] = "\n".join([f for f in address_fields if f])
        info['postcode'] = " ".join(
            council_data.get('postalcode', '').split(' ')[-2:])

        return info

    def handle(self, **options):
        """
        Manually run system checks for the
        'councils' and 'pollingstations' apps
        Management commands can ignore checks that only apply to
        the apps supporting the website part of the project
        """
        self.check([
            apps.get_app_config('councils'),
            apps.get_app_config('pollingstations')
        ])

        if options['teardown']:
            self.stdout.write('Clearing councils table..')
            Council.objects.all().delete()

        boundaries_url = settings.BOUNDARIES_URL
        if options['alt_url']:
            boundaries_url = options['alt_url']

        councils = []
        self.stdout.write("Downloading ONS boundaries from %s..." % (boundaries_url))
        councils = councils + self.get_councils(
            boundaries_url, id_field='lad16cd', name_field='lad16nm')

        for council in councils:
            self.stdout.write("Getting contact info for %s from YourVoteMatters" %\
                (council.council_id))
            info = self.get_contact_info_from_yvm(council.council_id)
            council.name = info['name']
            council.website = info['website']
            council.email = info['email']
            council.phone = info['phone']
            council.address = info['address']
            council.postcode = info['postcode']
            self._save_council(council)

        self.stdout.write('..done')
