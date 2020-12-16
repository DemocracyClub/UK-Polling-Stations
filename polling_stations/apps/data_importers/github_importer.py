import abc
import json
import tempfile
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.gdal import DataSource
from django.utils.encoding import force_bytes
from data_importers.base_importers import BaseGenericApiImporter


class BaseGitHubImporter(BaseGenericApiImporter, metaclass=abc.ABCMeta):

    base_url = "https://raw.githubusercontent.com/wdiv-scrapers/data/master/%s/%s.%s"
    stations_query = "stations"
    districts_query = "districts"
    stations_filetype = "json"
    districts_filetype = "json"
    srid = 4326
    districts_srid = 4326

    @property
    def stations_url(self):
        return self.base_url % (
            self.council_id,
            self.stations_query,
            self.stations_filetype,
        )

    @property
    def districts_url(self):
        return self.base_url % (
            self.council_id,
            self.districts_query,
            self.districts_filetype,
        )

    def extract_geometry(self, record, format, srid):
        if format == "geojson":
            return self.extract_json_geometry(record, srid)
        elif format == "gml":
            return self.extract_gml_geometry(record, srid)
        else:
            raise ValueError("Unsupported format: %s" % (format))

    def extract_json_geometry(self, record, srid):
        geom = json.loads(record["geometry"])
        if geom["geometry"] is None:
            return None
        geojson = json.dumps(geom["geometry"])
        poly = self.clean_poly(GEOSGeometry(geojson))
        poly.srid = srid
        return poly

    def extract_gml_geometry(self, record, srid):
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(force_bytes(record["geometry"]))
            tmp.seek(0)
            ds = DataSource(tmp.name)
            if len(ds[0]) == 1:
                wkt = next(iter(ds[0])).geom.wkt
                return self.clean_poly(GEOSGeometry(wkt, srid=srid))
            else:
                raise ValueError("Expected 1 feature, found %i" % len(ds[0]))
