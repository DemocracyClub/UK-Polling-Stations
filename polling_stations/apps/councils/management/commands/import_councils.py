import time

import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point

from councils.models import Council
from data_collection import constants
from data_finder.helpers import geocode


class Command(BaseCommand):
    def handle(self, **options):
        for council_type in constants.COUNCIL_TYPES:
            self.get_type_from_mapit(council_type)

    def get_wkt_from_mapit(self, area_id):
        req = requests.get('%sarea/%s.wkt' % (constants.MAPIT_URL, area_id))
        area = req.text
        if area.startswith('POLYGON'):
            area = area[7:]
            area = "MULTIPOLYGON(%s)" % area
        return GEOSGeometry(area, srid=27700)
        return area

    def get_contact_info_from_gov_uk(self, council_id):
        req = requests.get("%s%s" % (constants.GOV_UK_LA_URL, council_id))
        soup = BeautifulSoup(req.text)
        info = {}
        article = soup.findAll('article')[0]
        info['website'] = article.find(id='url')['href'].strip()
        info['email'] = article.find(
            id='authority_email').a['href'].strip()[7:]
        info['phone'] = article.find(id='authority_phone').text.strip()[7:]
        info['address'] = "\n".join(
            article.find(id='authority_address').stripped_strings)
        info['postcode'] = article.find(id='authority_postcode').text
        return info

    def get_type_from_mapit(self, council_type):
        req = requests.get('%sareas/%s' % (constants.MAPIT_URL, council_type))
        for mapit_id, council in list(req.json().items()):
            council_id = council['codes'].get('gss')
            if not council_id:
                council_id = council['codes'].get('ons')
            print(council_id)
            contact_info = {
                'name': council['name'],
            }
            if council_type != "LGD":
                contact_info.update(
                    self.get_contact_info_from_gov_uk(council_id))
            council, created = Council.objects.update_or_create(
                pk=council_id,
                mapit_id=mapit_id,
                council_type=council_type,
                defaults=contact_info,
            )
            if not council.area:
                council.area = self.get_wkt_from_mapit(mapit_id)
                council.save()
                time.sleep(1)
            if not council.location:
                print(council.postcode)
                try:
                    l = geocode(council.postcode)
                except:
                    continue
                time.sleep(1)
                council.location = Point(l['wgs84_lon'], l['wgs84_lat'])
                council.save()
