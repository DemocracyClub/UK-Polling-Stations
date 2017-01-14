import time

import requests
from bs4 import BeautifulSoup

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
            self.get_type_from_mapit(council_type)

    def _save_council(self, council):
        for db in settings.DATABASES.keys():
            council.save(using=db)

    def get_wkt_from_mapit(self, area_id):
        req = requests.get('%sarea/%s.wkt' % (settings.MAPIT_URL, area_id))
        area = req.text
        if area.startswith('POLYGON'):
            area = area[7:]
            area = "MULTIPOLYGON(%s)" % area
        return GEOSGeometry(area, srid=27700)
        return area

    def get_contact_info_from_gov_uk(self, council_id):
        if council_id.startswith('N'):
            # GOV.UK returns a 500 for any id in Northen Ireland
            return {}
        req = requests.get("%s%s" % (settings.GOV_UK_LA_URL, council_id))
        soup = BeautifulSoup(req.text, "lxml")
        info = {}
        article = soup.findAll('article')[0]
        try:
            info['website'] = article.find(id='url')['href'].strip()
        except TypeError:
            pass
        info['email'] = article.find(
            id='authority_email').a['href'].strip()[7:]
        info['phone'] = article.find(id='authority_phone').text.strip()[7:]
        info['address'] = "\n".join(
            article.find(id='authority_address').stripped_strings)
        info['postcode'] = article.find(id='authority_postcode').text
        return info

    def get_type_from_mapit(self, council_type):
        req = requests.get('%sareas/%s' % (settings.MAPIT_URL, council_type))
        for mapit_id, council in list(req.json().items()):
            council_id = council['codes'].get('gss')
            if not council_id:
                council_id = council['codes'].get('ons')
            print(council_id)
            defaults = {
                'name': council['name'],
            }
            defaults.update(
                self.get_contact_info_from_gov_uk(council_id))

            defaults['council_type'] = council_type
            defaults['mapit_id']= mapit_id

            council, created = Council.objects.update_or_create(
                pk=council_id,
                defaults=defaults,
            )

            # Call _save here to ensure it gets written to all databases
            self._save_council(council)

            if not council.area:
                council.area = self.get_wkt_from_mapit(mapit_id)
                self._save_council(council)
                time.sleep(1)
            if not council.location:
                print(council.postcode)
                try:
                    l = geocode(council.postcode)
                except:
                    continue
                time.sleep(1)
                council.location = Point(l['wgs84_lon'], l['wgs84_lat'])
                self._save_council(council)
