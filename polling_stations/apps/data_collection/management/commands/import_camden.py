"""
Imports Camden
"""
import tempfile
import urllib.request
from fastkml import kml
from django.contrib.gis.geos import GEOSGeometry, Point
from data_collection.base_importers import BaseGenericApiImporter, CsvMixin
from data_collection.geo_utils import convert_linestring_to_multiploygon


class Command(BaseGenericApiImporter, CsvMixin):
    """
    Imports the Polling Station data from Camden Council
    """

    stations_filetype = "csv"
    districts_filetype = "kml"
    srid = 4326
    districts_srid = 4326
    council_id = "E09000007"
    districts_url = "https://raw.githubusercontent.com/wdiv-scrapers/data/master/E09000007/districts.kml"
    stations_url = "https://raw.githubusercontent.com/wdiv-scrapers/data/master/E09000007/stations.csv"
    elections = ["parl.2019-12-12"]

    def parse_kml_features(self, data):
        k = kml.KML()
        k.from_string(data.encode("utf-8"))
        document = next(k.features())
        folder = next(document.features())
        return list(folder.features())

    def parse_extended_data(self, record):
        extended_data = {}
        for pair in record.extended_data.elements:
            if not pair.value:
                extended_data[pair.name] = ""
            else:
                extended_data[pair.name] = pair.value
        return extended_data

    def get_districts(self):
        with tempfile.NamedTemporaryFile() as tmp:
            urllib.request.urlretrieve(self.districts_url, tmp.name)
            data = open(tmp.name, "r").read()
            return self.parse_kml_features(data)

    def district_record_to_dict(self, record):

        # polygon
        geometry_collection = self.clean_poly(
            GEOSGeometry(record.geometry.wkt, srid=self.get_srid("districts"))
        )
        poly = GEOSGeometry(
            convert_linestring_to_multiploygon(geometry_collection),
            srid=self.get_srid("districts"),
        )

        # meta-data
        extended_data = self.parse_extended_data(record)
        district_id = str(extended_data["polling_district_code"]).strip()

        return {
            "internal_council_id": district_id,
            "name": "Camden - %s" % (district_id),
            "area": poly,
            "polling_station_id": district_id,
        }

    def station_record_to_dict(self, record):
        address = "\n".join([record.organisation, record.street])

        location = Point(
            float(record.longitude), float(record.latitude), srid=self.get_srid()
        )

        # user error report #227
        if (
            record.polling_district_name == "PB"
            and record.organisation == "Kings Cross Neighbourhood Community Centre"
        ):
            location = None

        return {
            "internal_council_id": record.polling_district_name,
            "postcode": record.postcode,
            "address": address,
            "location": location,
        }
