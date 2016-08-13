"""
Defines the base importer classes to implement
"""
import abc
import json
import glob
import os
import re
import tempfile
import unicodedata
import urllib.request

from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.gis import geos
from django.contrib.gis.geos import Point, GEOSGeometry
from django.db import connection
from django.db import transaction
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from councils.models import Council
from data_collection.data_quality_report import (
    DataQualityReportBuilder,
    StationReport,
    DistrictReport,
    ResidentialAddressReport
)
from data_collection.filehelpers import FileHelperFactory
from pollingstations.models import (
    PollingStation,
    PollingDistrict,
    ResidentialAddress
)
from data_collection.models import DataQuality
from addressbase.helpers import create_address_records_for_council


class Database:

    def teardown(self, council):
        PollingStation.objects.filter(council=council).delete()
        PollingDistrict.objects.filter(council=council).delete()
        ResidentialAddress.objects.filter(council=council).delete()

    def get_council(self, council_id):
        return Council.objects.get(pk=council_id)


class StationList:

    stations = []

    def __init__(self):
        self.stations = []

    def add(self, station):
        self.stations.append(station)

    def save(self):
        # make this more efficient
        for station in self.stations:
            PollingStation.objects.update_or_create(
                council=station['council'],
                internal_council_id=station['internal_council_id'],
                defaults=station,
            )


class DistrictList:

    districts = []

    def __init__(self):
        self.districts = []

    def add(self, district):
        self.districts.append(district)

    def save(self):
        # make this more efficient
        for district in self.districts:
            PollingDistrict.objects.update_or_create(
                council=district['council'],
                internal_council_id=district.get(
                    'internal_council_id', 'none'),
                defaults=district,
            )


class AddressList:

    addresses = []

    def __init__(self):
        self.addresses = []

    def add(self, address):
        self.addresses.append(address)

    def save(self):
        # make this more efficient
        for address in self.addresses:
            ResidentialAddress.objects.update_or_create(
                slug=address['slug'],
                defaults={
                    'council': address['council'],
                    'address': address['address'],
                    'postcode': address['postcode'],
                    'polling_station_id': address['polling_station_id'],
                }
            )


class PostProcessingMixin:

    def clean_postcodes_overlapping_districts(self):
        data = create_address_records_for_council(self.council)
        self.postcodes_contained_by_district = data['no_attention_needed']
        self.postcodes_with_addresses_generated = data['addresses_created']

    @transaction.atomic
    def clean_ambiguous_addresses(self):
        table_name = ResidentialAddress()._meta.db_table
        cursor = connection.cursor()
        cursor.execute("""
        DELETE FROM {0} WHERE CONCAT(address, postcode) IN (
         SELECT concat_address FROM (
             SELECT CONCAT(address, postcode) AS concat_address, COUNT(*) AS c
             FROM {0}
             WHERE council_id=%s
             GROUP BY CONCAT(address, postcode)
            ) as dupes
            WHERE dupes.c > 1
        )
        """.format(table_name), [self.council_id])


class BaseImporter(BaseCommand, PostProcessingMixin, metaclass=abc.ABCMeta):
    srid = 27700
    districts_srid = None
    council_id = None
    base_folder_path = None
    csv_encoding = 'utf-8'
    csv_delimiter = ','
    db = Database()

    def get_srid(self, type=None):
        if type == 'districts' and self.districts_srid is not None:
            return self.districts_srid
        else:
            return self.srid

    @abc.abstractmethod
    def import_data(self):
        pass

    def post_import(self):
        raise NotImplementedError

    def report(self):
        # build report
        report = DataQualityReportBuilder(self.council_id)
        station_report = StationReport(self.council_id)
        district_report = DistrictReport(self.council_id)
        address_report = ResidentialAddressReport(self.council_id)
        report.build_report()

        # save a static copy in the DB that we can serve up on the website
        record = DataQuality.objects.get_or_create(
            council_id=self.council_id,
        )
        record[0].report = report.generate_string_report()
        record[0].num_stations = station_report.get_stations_imported()
        record[0].num_districts = district_report.get_districts_imported()
        record[0].num_addresses = address_report.get_addresses_imported()
        record[0].save()

        # output to console
        report.output_console_report()

    @property
    def data_path(self):
        data_private = getattr(self, 'private', False)
        if data_private:
            path = getattr(
                settings,
                'PRIVATE_DATA_PATH',
                '../polling_station_data/')
        else:
            path = "./"
        return os.path.abspath(path)

    def handle(self, *args, **kwargs):
        if self.council_id is None:
            self.council_id = args[0]

        self.council = self.db.get_council(self.council_id)

        # Delete old data for this council
        self.db.teardown(self.council)

        if getattr(self, 'local_files', True):
            if self.base_folder_path is None:
                path = os.path.join(
                    self.data_path,
                    'data/{0}-*'.format(self.council_id))
                self.base_folder_path = glob.glob(path)[0]

        self.import_data()

        # Optional step for post import tasks
        try:
            self.post_import()
        except NotImplementedError:
            pass

        self.clean_ambiguous_addresses()

        # For areas with shape data, use AddressBase
        # to clean up overlapping postcode
        self.clean_postcodes_overlapping_districts()

        # save and output data quality report
        self.report()


class BaseStationsImporter(BaseImporter, metaclass=abc.ABCMeta):

    stations = None

    @property
    @abc.abstractmethod
    def stations_filetype(self):
        pass

    @property
    @abc.abstractmethod
    def stations_name(self):
        pass

    def get_stations(self):
        stations_file = os.path.join(self.base_folder_path, self.stations_name)
        options = {
            'encoding': self.csv_encoding,
            'delimiter': self.csv_delimiter
        }
        helper = FileHelperFactory.create(self.stations_filetype, stations_file, options)
        data = helper.get_features()
        return data

    @abc.abstractmethod
    def station_record_to_dict(self, record):
        pass

    def get_station_hash(self, station):
        raise NotImplementedError

    def import_polling_stations(self):
        stations = self.get_stations()
        seen = set()
        for station in stations:
            """
            We can optionally define a function get_station_hash()

            This is useful if residential addresses and polling
            station details are embedded in the same input file

            We can use this to avoid calling station_record_to_dict()
            (which is potentially quite a slow operation)
            on a record where we have already processed the station data
            to make the import process run more quickly.
            """
            try:
                station_hash = self.get_station_hash(station)
                if station_hash in seen:
                    continue
                else:
                    seen.add(station_hash)
            except NotImplementedError:
                pass

            if self.stations_filetype == 'shp':
                station_info = self.station_record_to_dict(station.record)
            else:
                station_info = self.station_record_to_dict(station)

            """
            station_record_to_dict() may optionally return None
            if we want to exclude a particular station record
            from being imported
            """
            if station_info is None:
                continue

            """
            station_record_to_dict() will usually return a dict
            but it may also optionally return a list of dicts.

            This is helpful if we encounter a polling station record
            with a delimited list of polling districts served by this
            polling station: it allows us to add the same station
            address/point many times with different district ids.
            """
            if isinstance(station_info, list):
                station_records = station_info
            else:
                # If station_info is a dict, create a singleton list
                station_records = [station_info]

            for station_record in station_records:
                if 'council' not in station_record:
                    station_record['council'] = self.council

                """
                If the file type is shp, we can usually derive 'location'
                automatically, but we can return it if necessary.
                For other file types, we must return the key
                'location' from station_record_to_dict()
                """
                if self.stations_filetype == 'shp' and 'location' not in station_record:
                    station_record['location'] = Point(
                        *station.shape.points[0],
                        srid=self.get_srid())

                self.add_polling_station(station_record)

    def add_polling_station(self, station_info):
        self.stations.add(station_info)


class BaseDistrictsImporter(BaseImporter, metaclass=abc.ABCMeta):

    districts = None

    @property
    @abc.abstractmethod
    def districts_filetype(self):
        pass

    @property
    @abc.abstractmethod
    def districts_name(self):
        pass

    def get_districts(self):
        districts_file = os.path.join(self.base_folder_path, self.districts_name)
        options = {}
        helper = FileHelperFactory.create(self.districts_filetype, districts_file, options)
        data = helper.get_features()
        return data

    def clean_poly(self, poly):
        if isinstance(poly, geos.Polygon):
            poly = geos.MultiPolygon(poly, srid=self.get_srid('districts'))
            return poly
        return poly

    def strip_z_values(self, geojson):
        districts = json.loads(geojson)
        districts['type'] = 'Polygon'
        for points in districts['coordinates'][0][0]:
            if len(points) == 3:
                points.pop()
        districts['coordinates'] = districts['coordinates'][0]
        return json.dumps(districts)

    @abc.abstractmethod
    def district_record_to_dict(self, record):
        pass

    def import_polling_districts(self):
        districts = self.get_districts()
        for district in districts:
            if self.districts_filetype == 'shp':
                district_info = self.district_record_to_dict(district.record)
            else:
                district_info = self.district_record_to_dict(district)

            """
            district_record_to_dict() may optionally return None
            if we want to exclude a particular district record
            from being imported
            """
            if district_info is None:
                continue

            if 'council' not in district_info:
                district_info['council'] = self.council

            """
            If the file type is shp or json, we can usually derive
            'area' automatically, but we can return it if necessary.
            For other file types, we must return the key
            'area' from address_record_to_dict()
            """
            if self.districts_filetype == 'shp':
                geojson = json.dumps(district.shape.__geo_interface__)
            if self.districts_filetype == 'json':
                geojson = json.dumps(district['geometry'])
            if 'location' not in district_info and\
                (self.districts_filetype == 'shp' or\
                self.districts_filetype == 'json'):
                poly = self.clean_poly(
                    GEOSGeometry(geojson, srid=self.get_srid('districts')))
                district_info['area'] = poly

            self.add_polling_district(district_info)

    def add_polling_district(self, district_info):
        self.districts.add(district_info)


class BaseAddressesImporter(BaseImporter, metaclass=abc.ABCMeta):

    addresses = None

    @property
    @abc.abstractmethod
    def addresses_filetype(self):
        pass

    @property
    @abc.abstractmethod
    def addresses_name(self):
        pass

    def get_addresses(self):
        addresses_file = os.path.join(self.base_folder_path, self.addresses_name)
        options = {
            'encoding': self.csv_encoding,
            'delimiter': self.csv_delimiter
        }
        helper = FileHelperFactory.create(self.addresses_filetype, addresses_file, options)
        data = helper.get_features()
        return data

    def slugify(self, value):
        """
        Custom slugify function:

        Convert to ASCII.
        Convert characters that aren't alphanumerics, underscores,
        or hyphens to hyphens
        Convert to lowercase.
        Strip leading and trailing whitespace.

        Unfortunately it is necessary to create wheel 2.0 in this situation
        because using django's standard slugify() function means that
        '1/2 Foo Street' and '12 Foo Street' both slugify to '12-foo-street'.
        This ensures that
        '1/2 Foo Street' becomes '1-2-foo-street' and
        '12 Foo Street' becomes '12-foo-street'

        This means we can avoid appending an arbitrary number and minimise
        disruption to the public URL schema if a council provides updated data
        """
        value = force_text(value)
        value = unicodedata.normalize(
            'NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub('[^\w\s-]', '-', value).strip().lower()
        return mark_safe(re.sub('[-\s]+', '-', value))

    def get_slug(self, address_info):
        # if we have a uprn, use that as the slug
        if 'uprn' in address_info:
            if address_info['uprn']:
                return address_info['uprn']

        # otherwise build a slug from the other data we have
        return self.slugify(
            "%s-%s-%s-%s" % (
                self.council.pk,
                address_info['polling_station_id'],
                address_info['address'],
                address_info['postcode']
            )
        )

    @abc.abstractmethod
    def address_record_to_dict(self, record):
        pass

    def import_residential_addresses(self):
        addresses = self.get_addresses()
        for address in addresses:
            address_info = self.address_record_to_dict(address)
            if address_info is None:
                continue
            if 'council' not in address_info:
                address_info['council'] = self.council
            self.add_residential_address(address_info)

    def add_residential_address(self, address_info):

        """
        strip all whitespace from postcode and convert to uppercase
        this will make it easier to query this based on user-supplied postcode
        """
        address_info['postcode'] =\
            re.sub('[^A-Z0-9]', '', address_info['postcode'].upper())

        # generate a unique slug so we can provide a consistent url
        slug = self.get_slug(address_info)
        address_info['slug'] = slug

        self.addresses.add(address_info)


class BaseStationsDistrictsImporter(
    BaseStationsImporter, BaseDistrictsImporter):

    def import_data(self):
        self.stations = StationList()
        self.districts = DistrictList()
        self.import_polling_districts()
        self.import_polling_stations()
        self.districts.save()
        self.stations.save()


class BaseStationsAddressesImporter(
    BaseStationsImporter, BaseAddressesImporter):

    def import_data(self):
        self.stations = StationList()
        self.addresses = AddressList()
        self.import_residential_addresses()
        self.import_polling_stations()
        self.addresses.save()
        self.stations.save()


"""
Stations in CSV format
Districts in SHP format
"""
class BaseCsvStationsShpDistrictsImporter(BaseStationsDistrictsImporter):

    stations_filetype = 'csv'
    districts_filetype = 'shp'


"""
Stations in SHP format
Districts in SHP format
"""
class BaseShpStationsShpDistrictsImporter(BaseStationsDistrictsImporter):

    stations_filetype = 'shp'
    districts_filetype = 'shp'


"""
Stations in CSV format
Districts in JSON format
"""
class BaseCsvStationsJsonDistrictsImporter(BaseStationsDistrictsImporter):

    stations_filetype = 'csv'
    districts_filetype = 'json'


"""
Stations in CSV format
Districts in KML format
"""
class BaseCsvStationsKmlDistrictsImporter(BaseStationsDistrictsImporter):

    districts_srid = 4326
    stations_filetype = 'csv'
    districts_filetype = 'kml'

    # this is mainly here for legacy compatibility
    # mostly we should override this
    def district_record_to_dict(self, record):
        geojson = self.strip_z_values(record.geom.geojson)
        poly = self.clean_poly(
            GEOSGeometry(geojson, srid=self.get_srid('districts')))
        return {
            'internal_council_id': record['Name'].value,
            'name': record['Name'].value,
            'area': poly
        }


"""
Stations in CSV format
Addresses in CSV format
"""
class BaseCsvStationsCsvAddressesImporter(BaseStationsAddressesImporter):

    stations_filetype = 'csv'
    addresses_filetype = 'csv'


"""
Stations in SHP format
Addresses in CSV format
"""
class BaseShpStationsCsvAddressesImporter(BaseStationsAddressesImporter):

    stations_filetype = 'shp'
    addresses_filetype = 'csv'


class BaseGenericApiImporter(BaseStationsDistrictsImporter):
    srid = 4326
    districts_srid = 4326
    districts_url = None
    stations_url = None
    local_files = False

    def import_data(self):
        self.districts = DistrictList()
        self.stations = StationList()

        # deal with 'stations only' or 'districts only' data
        if self.districts_url is not None:
            self.import_polling_districts()
        if self.stations_url is not None:
            self.import_polling_stations()

        self.districts.save()
        self.stations.save()

    def get_districts(self):
        with tempfile.NamedTemporaryFile() as tmp:
            req = urllib.request.urlretrieve(self.districts_url, tmp.name)
            options = {}
            helper = FileHelperFactory.create(self.districts_filetype, tmp.name, options)
            data = helper.get_features()
            return data

    def get_stations(self):
        with tempfile.NamedTemporaryFile() as tmp:
            req = urllib.request.urlretrieve(self.stations_url, tmp.name)
            options = {}
            helper = FileHelperFactory.create(self.stations_filetype, tmp.name, options)
            data = helper.get_features()
            return data


"""
Stations in KML format
Districts in KML format
"""
class BaseApiKmlStationsKmlDistrictsImporter(BaseGenericApiImporter):

    stations_filetype = 'kml'
    districts_filetype = 'kml'
