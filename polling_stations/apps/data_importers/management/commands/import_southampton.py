"""
Imports Southampton
"""
from lxml import etree
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Point
from data_importers.management.commands import BaseApiKmlStationsKmlDistrictsImporter


class Command(BaseApiKmlStationsKmlDistrictsImporter):
    """
    Imports the Polling Station data from Southampton
    """

    srid = 4326
    districts_srid = 4326
    council_id = "E06000045"
    districts_url = "https://raw.githubusercontent.com/wdiv-scrapers/data/master/E06000045/districts.kml"
    stations_url = "https://raw.githubusercontent.com/wdiv-scrapers/data/master/E06000045/stations.kml"
    elections = ["2020-05-07"]

    def extract_info_from_district_description(self, description):
        # lxml needs everything to be enclosed in one root element
        html = etree.XML("<div>" + str(description).replace("&", "&amp;") + "</div>")
        return {
            "POLLING_DISTRICT_REF": html[1][0][1].text,
            "WARD_NAME": html[1][1][1].text,
            "TOTAL_ELECTORATE": html[1][2][1].text,
            "MI_PRINX": html[1][3][1].text,
        }

    def district_record_to_dict(self, record):
        # polygon
        geojson = record.geom.geojson
        geometry_collection = self.clean_poly(
            GEOSGeometry(geojson, srid=self.get_srid("districts"))
        )

        try:
            poly = MultiPolygon(
                geometry_collection[-1], srid=self.get_srid("districts")
            )
        except TypeError:
            poly = geometry_collection[-1]

        # metadata
        info = self.extract_info_from_district_description(record["description"])

        return {
            "internal_council_id": info["POLLING_DISTRICT_REF"],
            "name": "%s - %s" % (info["WARD_NAME"], info["POLLING_DISTRICT_REF"]),
            "area": poly,
        }

    def extract_info_from_station_description(self, description):
        # lxml needs everything to be enclosed in one root element
        html = etree.XML("<div>" + str(description).replace("&", "&amp;") + "</div>")
        return {
            "POLLING_STATION": html[0][0][0].text,
            "POLLING_DISTRICT_REF": html[0][1][0].text.split(":")[1].strip(),
        }

    def station_record_to_dict(self, record):
        # point
        geojson = record.geom.geojson
        location = GEOSGeometry(geojson, srid=self.get_srid())

        # metadata
        info = self.extract_info_from_station_description(record["description"])

        # format address
        address = info["POLLING_STATION"]
        address_parts = address.split(", ")
        if address_parts[-1][:2] == "SO":
            postcode = address_parts[-1]
            del address_parts[-1]
        else:
            postcode = ""
        address = "\n".join(address_parts)

        code = info["POLLING_DISTRICT_REF"]
        # fiddle a couple of points slightly to make the directions work better
        # user issue report #98
        if code == "CA" and address.startswith("Avenue Hall at Avenue St"):
            location = Point(-1.404693, 50.921401, srid=4326)
        # user issue report #119
        if code == "GC" and address.startswith("Banister Primary School"):
            location = Point(-1.409071, 50.916527, srid=4326)

        return {
            "internal_council_id": code,
            "postcode": postcode,
            "address": address,
            "location": location,
            "polling_district_id": code,
        }
