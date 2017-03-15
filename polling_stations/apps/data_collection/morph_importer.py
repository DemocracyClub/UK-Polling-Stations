import abc
import json
import tempfile
from django.apps import apps
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.gdal import DataSource
from django.core.checks import Error, register
from django.utils.encoding import force_bytes
from data_collection.base_importers import BaseGenericApiImporter


@register()
def api_key_check(app_configs, **kwargs):
    errors = []

    if (app_configs is None or\
        apps.get_app_config('data_collection') in app_configs):

        key = getattr(settings, 'MORPH_API_KEY', '')
        if key == '':
            errors.append(
                Error(
                    'MORPH_API_KEY must be set',
                    hint='Define MORPH_API_KEY as an env var or in local.py',
                    obj='BaseMorphApiImporter',
                    id='data_collection.E001',
                )
            )
    return errors


class BaseMorphApiImporter(BaseGenericApiImporter, metaclass=abc.ABCMeta):

    base_url = 'https://api.morph.io/'
    stations_query = '/data.json?query=select%20*%20from%20%27stations%27%3B'
    districts_query = '/data.json?query=select%20*%20from%20%27districts%27%3B'
    stations_filetype = 'json'
    districts_filetype = 'json'
    srid = 4326
    districts_srid = 4326

    @property
    @abc.abstractmethod
    def scraper_name(self):
        pass

    @property
    def morph_api_key(self):
        return settings.MORPH_API_KEY

    @property
    def stations_url(self):
        return "%s%s%s&key=%s" % (
            self.base_url, self.scraper_name, self.stations_query, self.morph_api_key)

    @property
    def districts_url(self):
        return "%s%s%s&key=%s" % (
            self.base_url, self.scraper_name, self.districts_query, self.morph_api_key)

    def extract_geometry(self, record, format, srid):
        if format == 'geojson':
            return self.extract_json_geometry(record, srid)
        elif format == 'gml':
            return self.extract_gml_geometry(record, srid)
        else:
            raise ValueError("Unsupported format: %s" % (format))

    def extract_json_geometry(self, record, srid):
        geom = json.loads(record['geometry'])
        geojson = json.dumps(geom['geometry'])
        return self.clean_poly(GEOSGeometry(geojson, srid=srid))

    def extract_gml_geometry(self, record, srid):
        """
        This is a bit of a hack

        In this version of Django, there is no way to directly create an
        OGRGeometry or GEOSGeometry object directly from a GML string but we
        can do it by writing it out to a file and then reading it back in with
        DataSource().

        This functionality will be added in Django 1.11
        https://docs.djangoproject.com/en/dev/releases/1.11/#django-contrib-gis
        """

        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(force_bytes(record['geometry']))
            tmp.seek(0)
            try:
                ds = DataSource(tmp.name)
            except:
                ds = DataSource(tmp.name)
            if len(ds[0]) == 1:
                geojson = next(iter(ds[0])).geom.geojson
                return self.clean_poly(GEOSGeometry(geojson, srid=srid))
            else:
                raise ValueError("Expected 1 feature, found %i" % len(ds[0]))
