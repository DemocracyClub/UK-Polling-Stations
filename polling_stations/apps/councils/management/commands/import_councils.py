import html
import time
import json

import requests

from django.apps import apps
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point
from django.conf import settings

from councils.models import Council
from data_finder.helpers import geocode


class Command(BaseCommand):
    """
    Turn off auto system check for all apps
    We will maunally run system checks only for the
    'councils' and 'pollingstations' apps
    """
    requires_system_checks = False

    headers = {}
    if settings.MAPIT_UA:
        headers['User-Agent'] = settings.MAPIT_UA

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--nosleep',
            default=False,
            action='store_true',
            required=False,
            help="Don't sleep between requests"
        )

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

        for council_type in settings.COUNCIL_TYPES:
            self.get_type_from_mapit(council_type, options['nosleep'])

    def _save_council(self, council):
        for db in settings.DATABASES.keys():
            council.save(using=db)

    def get_wkt_from_mapit(self, area_id):
        req = requests.get(
            '%sarea/%s.wkt' % (settings.MAPIT_URL, area_id),
            headers=self.headers)
        area = req.text
        if area.startswith('POLYGON'):
            area = area[7:]
            area = "MULTIPOLYGON(%s)" % area
        return GEOSGeometry(area, srid=27700)

    def clean_url(self, url):
        if not url.startswith(('http://', 'https://')):
            # Assume http everywhere will redirect to https if it's there.
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

    def get_type_from_mapit(self, council_type, nosleep):
        req = requests.get(
            '%sareas/%s' % (settings.MAPIT_URL, council_type),
            headers=self.headers)
        # Sort here so the fixtures work as expected in tests
        areas = sorted(req.json().items(), key=lambda data: int(data[0]))
        for mapit_id, council in areas:
            council_id = council['codes'].get('gss')
            if not council_id:
                council_id = council['codes'].get('ons')
            print(council_id)

            defaults = self.get_contact_info_from_yvm(council_id)

            defaults['council_type'] = council_type
            defaults['mapit_id'] = mapit_id

            council, created = Council.objects.update_or_create(
                pk=council_id,
                defaults=defaults,
            )

            # Call _save here to ensure it gets written to all databases
            self._save_council(council)

            if not council.area:
                council.area = self.get_wkt_from_mapit(mapit_id)
                self._save_council(council)
                if not nosleep or not self.headers:
                    time.sleep(1)
            if not council.location:
                print(council.postcode)
                try:
                    l = geocode(council.postcode)
                except:
                    continue
                if not nosleep or not self.headers:
                    time.sleep(1)
                council.location = Point(l['wgs84_lon'], l['wgs84_lat'])
                self._save_council(council)
