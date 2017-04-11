"""
NOTE:
Daventry's mapping server return KMLs which has the meta-data in
`<ExtendedData>` tags but doesn't declare an ExtendedData Schema in the header.
This is technically valid according to the KML 2.2 spec, but Django's GDAL
wrappers don't make ExtendedData available unless there is a schema defined in
the header. To solve this, I've used fastkml instead as this implements a more
lenient interpretation of the spec which allows us access to the meta-data.
"""
import requests
from fastkml import kml
from time import sleep
from django.contrib.gis.geos import GEOSGeometry, Point
from data_collection.geo_utils import convert_linestring_to_multiploygon
from data_collection.base_importers import BaseGenericApiImporter


class Command(BaseGenericApiImporter):
    srid = 4326
    districts_srid = 4326
    council_id = 'E07000151'
    districts_url = 'http://feeds.getmapping.com/47732.wmsx?login=61dfb362-893b-464d-8a96-fb3edb7565f8&password=yd5v5y03&LAYERS=daventry_parliamentary_polling_districts_region&TRANSPARENT=TRUE&HOVER=false&FORMAT=kml&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&CRS=EPSG%3A27700&BBOX=447025,247876,489247,288998&WIDTH=867&HEIGHT=426'
    stations_url = 'http://feeds.getmapping.com/47733.wmsx?login=70a1b086-b9cc-4b22-9b90-7d88bd589d4b&password=sjy2869b&LAYERS=daventry_parliamentary_polling_stations&TRANSPARENT=TRUE&HOVER=false&FORMAT=kml&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&CRS=EPSG%3A27700&BBOX=449708,250805,486927,287603&WIDTH=867&HEIGHT=426'
    #elections = ['local.northamptonshire.2017-05-04']
    elections = []
    duplicate_districts = set()
    districts_filetype = 'kml.extended'
    stations_filetype = 'kml.extended'

    def get_data(self, url):
        """
        Daventry's API seems to quite frequently return:

        <?xml version='1.0' encoding="UTF-8"?>
        <ServiceExceptionReport
            version="1.3.0"
            xmlns="http://www.opengis.net/ogc"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.opengis.net/ogc http://schemas.opengis.net/wms/1.3.0/exceptions_1_3_0.xsd">
            <ServiceException>
                <![CDATA[Error: Unable to respond to request.]]>
            </ServiceException>
        </ServiceExceptionReport>

        (with a handy `200 OK` status code!)
        We will try it a few times with sleeps to see if we can get a
        valid response back. If not, give up and chuck an exception.
        """
        for i in range(10):
            res = requests.get(url)
            if 'Unable to respond to request' not in res.text:
                return res.text
            sleep(10)  # give their server a few seconds to think
        raise ConnectionError('I tried, but it was no good :(')

    def parse_kml_features(self, data):
        k = kml.KML()
        k.from_string(data.encode('utf-8'))
        document = next(k.features())
        folder = next(document.features())
        return list(folder.features())

    def get_districts(self):
        res = self.get_data(self.districts_url)
        return self.parse_kml_features(res)

    def get_stations(self):
        res = self.get_data(self.stations_url)
        return self.parse_kml_features(res)

    def pre_import(self):
        self.find_duplicate_districts()

    def find_duplicate_districts(self):
        # identify any district codes which appear
        # more than once (with 2 different polygons)
        # We do not want to import these.
        seen = set()
        districts = self.get_districts()
        for district in districts:
            extended_data = self.parse_extended_data(district)
            if str(extended_data['pollingdis']) in seen:
                self.duplicate_districts.add(str(extended_data['pollingdis']))
            seen.add(str(extended_data['pollingdis']))

    def parse_extended_data(self, record):
        extended_data = {}
        for pair in record.extended_data.elements:
            if not pair.value:
                extended_data[pair.name] = ''
            else:
                extended_data[pair.name] = pair.value
        return extended_data

    def district_record_to_dict(self, record):

        # polygon
        geometry_collection = self.clean_poly(
            GEOSGeometry(record.geometry.wkt, srid=self.get_srid('districts'))
        )
        poly = convert_linestring_to_multiploygon(geometry_collection)

        # meta-data
        extended_data = self.parse_extended_data(record)
        district_id = str(extended_data['pollingdis']).strip()
        if district_id in self.duplicate_districts:
            return None
        else :
            return {
                'internal_council_id': district_id,
                'name': "%s - %s" % (extended_data['pollingdis'], extended_data['name']),
                'area': poly
            }

    def format_address(self, address_parts):
        address = "\n".join(address_parts)
        while "\n\n" in address:
            address = address.replace("\n\n", "\n")
        return address

    def station_record_to_dict(self, record):
        # point
        location = GEOSGeometry(record.geometry.wkt, srid=self.get_srid())

        # meta-data
        extended_data = self.parse_extended_data(record)

        # address
        address = self.format_address([
            str(extended_data['polling_st']),
            ("%s %s" % (str(extended_data['address1']), str(extended_data['address2']))).strip(),
            str(extended_data['locality']),
            str(extended_data['town_villa']),
        ])

        district_ids = str(extended_data['pollingdis']).strip().split(', ')
        stations = []
        for district_id in district_ids:
            stations.append({
                'internal_council_id': district_id,
                'postcode': extended_data['postcode'],
                'address': address,
                'location': location,
                'polling_district_id': district_id
            })
        return stations
