"""
Defines the base importer classes to implement
"""
import abc
import json
import glob
import logging
import os
import tempfile
import urllib.request

from argparse import ArgumentTypeError
from django.apps import apps
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.gis import geos
from django.contrib.gis.geos import Point, GEOSGeometry, GEOSException
from django.db import connection
from django.db import transaction

from councils.models import Council
from data_collection.data_types import (
    AddressSet,
    DistrictSet,
    StationSet
)
from data_collection.data_quality_report import (
    DataQualityReportBuilder,
    StationReport,
    DistrictReport,
    ResidentialAddressReport
)
from data_collection.contexthelpers import Dwellings
from data_collection.filehelpers import FileHelperFactory
from data_collection.loghelper import LogHelper
from data_collection.slugger import Slugger
from data_collection.s3wrapper import S3Wrapper
from pollingstations.models import (
    PollingStation,
    PollingDistrict,
    ResidentialAddress
)
from data_collection.models import DataQuality
from uk_geo_utils.helpers import Postcode
from addressbase.helpers import create_address_records_for_council


class PostProcessingMixin:

    def clean_postcodes_overlapping_districts(self, batch_size, logger):
        data = create_address_records_for_council(self.council, batch_size, logger)
        self.postcodes_contained_by_district = data['no_attention_needed']
        self.postcodes_with_addresses_generated = data['addresses_created']


class CsvMixin:
    csv_encoding = 'utf-8'
    csv_delimiter = ','

    def get_file_options(self):
        return {
            'encoding': self.csv_encoding,
            'delimiter': self.csv_delimiter
        }


class BaseImporter(BaseCommand, PostProcessingMixin, metaclass=abc.ABCMeta):

    """
    Turn off auto system check for all apps
    We will maunally run system checks only for the
    'data_collection' and 'pollingstations' apps
    """
    requires_system_checks = False

    srid = 27700
    council_id = None
    base_folder_path = None
    logger = None
    batch_size = None

    def write_info(self, message):
        if self.verbosity > 0:
            self.stdout.write(message)

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--noclean',
            help='<Optional> Do not run clean_postcodes_overlapping_districts()',
            action='store_true',
            required=False,
            default=False
        )

        def check_positive(value):
            ivalue = int(value)
            if ivalue < 1:
                raise ArgumentTypeError("%s is an invalid positive int value" % value)
            return ivalue

        parser.add_argument(
            '-b',
            '--batch_size',
            help='<Optional> Number of records to insert in each batch when importing addresses',
            type=check_positive,
            required=False,
            default=3000
        )

        parser.add_argument(
            '--nochecks',
            help='<Optional> Do not perform validation checks or display context information',
            action='store_true',
            required=False,
            default=False
        )

    def teardown(self, council):
        PollingStation.objects.filter(council=council).delete()
        PollingDistrict.objects.filter(council=council).delete()
        ResidentialAddress.objects.filter(council=council).delete()

    def get_council(self, council_id):
        return Council.objects.get(pk=council_id)

    def get_data(self, filetype, filename):
        if hasattr(self, 'get_file_options'):
            options = self.get_file_options()
        else:
            options = {}
        helper = FileHelperFactory.create(filetype, filename, options)
        return helper.get_features()

    def get_srid(self, type=None):
        if hasattr(self, 'districts_srid') and\
           type == 'districts' and\
           self.districts_srid is not None:
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
            s3 = S3Wrapper()
            s3.fetch_data_by_council(self.council_id)
            path = s3.data_path
        return os.path.abspath(path)

    def get_base_folder_path(self):
        if getattr(self, 'local_files', True):
            if self.base_folder_path is None:
                path = os.path.join(
                    self.data_path,
                    '{0}-*'.format(self.council_id))
                return glob.glob(path)[0]
        return self.base_folder_path

    def handle(self, *args, **kwargs):
        """
        Manually run system checks for the
        'data_collection' and 'pollingstations' apps
        Management commands can ignore checks that only apply to
        the apps supporting the website part of the project
        """
        self.check([
            apps.get_app_config('data_collection'),
            apps.get_app_config('pollingstations')
        ])

        self.verbosity = kwargs.get('verbosity')
        self.logger = LogHelper(self.verbosity)
        self.batch_size = kwargs.get('batch_size')
        self.validation_checks = not(kwargs.get('nochecks'))

        if self.council_id is None:
            self.council_id = args[0]

        self.council = self.get_council(self.council_id)
        self.write_info("Importing data for %s..." % self.council.name)

        # Delete old data for this council
        self.teardown(self.council)

        self.base_folder_path = self.get_base_folder_path()

        self.import_data()

        # Optional step for post import tasks
        try:
            self.post_import()
        except NotImplementedError:
            pass

        # For areas with shape data, use AddressBase
        # to clean up overlapping postcode
        if not kwargs.get('noclean'):
            self.clean_postcodes_overlapping_districts(self.batch_size, self.logger)

        # save and output data quality report
        if self.verbosity > 0:
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
        return self.get_data(self.stations_filetype, stations_file)

    @abc.abstractmethod
    def station_record_to_dict(self, record):
        pass

    def get_station_hash(self, station):
        raise NotImplementedError

    def check_station_point(self, station_record):
        if station_record['location']:
            try:
                council = Council.objects.get(area__covers=station_record['location'])
                if council.council_id != self.council_id:
                    self.logger.log_message(
                        logging.WARNING,
                        "Polling station %s is in %s (%s) but target council is %s (%s) - manual check recommended",
                        variable=(
                            station_record['internal_council_id'],
                            council.name,
                            council.council_id,
                            self.council.name,
                            self.council.council_id))
            except Council.DoesNotExist:
                self.logger.log_message(
                    logging.WARNING,
                    "Polling station %s is not covered by any council area - manual check recommended",
                    variable=(station_record['internal_council_id']))

    def import_polling_stations(self):
        stations = self.get_stations()
        if not isinstance(self, BaseAddressesImporter):
            self.write_info(
                "Stations: Found %i features in input file" % (len(stations)))
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
                    self.logger.log_message(
                        logging.INFO, "Polling station added to set:\n%s",
                        variable=station, pretty=True)
                    seen.add(station_hash)
            except NotImplementedError:
                pass

            if self.stations_filetype in ['shp', 'shp.zip']:
                record = station.record
            else:
                record = station
            station_info = self.station_record_to_dict(record)

            """
            station_record_to_dict() will usually return a dict
            but it may also optionally return a list of dicts.

            This is helpful if we encounter a polling station record
            with a delimited list of polling districts served by this
            polling station: it allows us to add the same station
            address/point many times with different district ids.
            """
            if isinstance(station_info, list):
                self.logger.log_message(
                    logging.INFO, "station_record_to_dict() returned list with input:\n%s",
                    variable=record, pretty=True)
                station_records = station_info
            else:
                # If station_info is a dict, create a singleton list
                station_records = [station_info]

            for station_record in station_records:

                """
                station_record_to_dict() may optionally return None
                if we want to exclude a particular station record
                from being imported
                """
                if station_record is None:
                    self.logger.log_message(
                        logging.INFO,
                        "station_record_to_dict() returned None with input:\n%s",
                        variable=record, pretty=True)
                    continue

                if 'council' not in station_record:
                    station_record['council'] = self.council

                """
                If the file type is shp, we can usually derive 'location'
                automatically, but we can return it if necessary.
                For other file types, we must return the key
                'location' from station_record_to_dict()
                """
                if self.stations_filetype in ['shp', 'shp.zip'] and 'location' not in station_record:
                    if len(station.shape.points) == 1:
                        # we've got a point
                        station_record['location'] = Point(
                            *station.shape.points[0],
                            srid=self.get_srid())
                    else:
                        # its a polygon: simplify it to a centroid and warn
                        self.logger.log_message(logging.WARNING,
                            "Implicitly converting station geometry to point")
                        geojson = json.dumps(station.shape.__geo_interface__)
                        poly = self.clean_poly(
                            GEOSGeometry(geojson, srid=self.get_srid()))
                        station_record['location'] = poly.centroid

                if self.validation_checks:
                    self.check_station_point(station_record)
                self.add_polling_station(station_record)

    def add_polling_station(self, station_info):
        self.stations.add(station_info)


class BaseDistrictsImporter(BaseImporter, metaclass=abc.ABCMeta):

    districts = None
    districts_srid = None

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
        return self.get_data(self.districts_filetype, districts_file)

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

    def check_district_overlap(self, district_record):
        if self.council.area.contains(district_record['area']):
            self.logger.log_message(
                logging.INFO,
                "District %s is fully contained by target local auth",
                variable=district_record['internal_council_id'])
            return 100

        try:
            intersection = self.council.area.intersection(
                district_record['area'].transform(4326, clone=True))
            district_area = district_record['area'].transform(27700, clone=True).area
            intersection_area = intersection.transform(27700, clone=True).area
        except GEOSException as e:
            self.logger.log_message(logging.ERROR, str(e))
            return

        overlap_percentage = (intersection_area/district_area)*100
        if overlap_percentage > 99:
            # meh - close enough
            level = logging.INFO
        else:
            level = logging.WARNING

        self.logger.log_message(
            level,
            "District {0} is {1:.2f}% contained by target local auth".format(
                district_record['internal_council_id'],
                overlap_percentage
            )
        )

        return overlap_percentage

    def import_polling_districts(self):
        districts = self.get_districts()
        self.write_info(
            "Districts: Found %i features in input file" % (len(districts)))
        for district in districts:
            if self.districts_filetype in ['shp', 'shp.zip']:
                district_info = self.district_record_to_dict(district.record)
            else:
                district_info = self.district_record_to_dict(district)

            """
            district_record_to_dict() may optionally return None
            if we want to exclude a particular district record
            from being imported
            """
            if district_info is None:
                self.logger.log_message(
                    logging.INFO,
                    "district_record_to_dict() returned None with input:\n%s",
                    variable=district, pretty=True)
                continue

            if 'council' not in district_info:
                district_info['council'] = self.council

            """
            If the file type is shp or geojson, we can usually derive
            'area' automatically, but we can return it if necessary.
            For other file types, we must return the key
            'area' from address_record_to_dict()
            """
            if self.districts_filetype in ['shp', 'shp.zip']:
                geojson = json.dumps(district.shape.__geo_interface__)
            if self.districts_filetype == 'geojson':
                geojson = json.dumps(district['geometry'])
            if 'area' not in district_info and\
                    (self.districts_filetype in ['shp', 'shp.zip', 'geojson']):
                poly = self.clean_poly(
                    GEOSGeometry(geojson, srid=self.get_srid('districts')))
                district_info['area'] = poly

            if self.validation_checks:
                self.check_district_overlap(district_info)
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
        return self.get_data(self.addresses_filetype, addresses_file)

    def get_slug(self, address_info):
        self.logger.log_message(logging.DEBUG, "Generating custom slug")
        return Slugger.slugify(
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

    def write_context_data(self):
        dwellings = Dwellings()
        self.write_info('----------------------------------')
        self.write_info('Contextual Data:')
        self.write_info("Total UPRNs in ONSUD: {:,}".format(
            dwellings.from_onsud(self.council_id))
        )
        self.write_info("Total UPRNs in AddressBase Standard: {:,}".format(
            dwellings.from_addressbase(self.council.area))
        )
        self.write_info("Total Dwellings from 2011 Census: {:,}".format(
            dwellings.from_census(self.council_id))
        )
        self.write_info('----------------------------------')

    def import_residential_addresses(self):
        if self.validation_checks:
            self.write_context_data()
        addresses = self.get_addresses()
        self.write_info(
            "Addresses: Found {:,} rows in input file".format(len(addresses)))
        for address in addresses:
            address_info = self.address_record_to_dict(address)

            if address_info is None:
                self.logger.log_message(
                    logging.INFO,
                    "address_record_to_dict() returned None with input:\n%s",
                    variable=address, pretty=True)
                continue

            self.add_residential_address(address_info)

    def add_residential_address(self, address_info):

        if 'council' not in address_info:
            address_info['council'] = self.council

        if 'uprn' not in address_info:
            address_info['uprn'] = ''
        else:
            address_info['uprn'] = str(address_info['uprn']).lstrip('0')

        address_info['postcode'] = Postcode(address_info['postcode']).without_space

        # generate a unique slug so we can provide a consistent url
        slug = self.get_slug(address_info)
        address_info['slug'] = slug

        self.addresses.add(address_info)


class BaseStationsDistrictsImporter(BaseStationsImporter,
                                    BaseDistrictsImporter):

    def pre_import(self):
        raise NotImplementedError

    def import_data(self):

        # Optional step for pre import tasks
        try:
            self.pre_import()
        except NotImplementedError:
            pass

        self.stations = StationSet()
        self.districts = DistrictSet()
        self.import_polling_districts()
        self.import_polling_stations()
        self.districts.save()
        self.stations.save()


class BaseStationsAddressesImporter(BaseStationsImporter,
                                    BaseAddressesImporter):

    def pre_import(self):
        raise NotImplementedError

    def import_data(self):

        # Optional step for pre import tasks
        try:
            self.pre_import()
        except NotImplementedError:
            pass

        self.stations = StationSet()
        self.addresses = AddressSet(self.logger)
        self.import_residential_addresses()
        self.import_polling_stations()
        self.addresses.save(self.batch_size)
        self.stations.save()


class BaseCsvStationsShpDistrictsImporter(BaseStationsDistrictsImporter,
                                          CsvMixin):
    """
    Stations in CSV format
    Districts in SHP format
    """

    stations_filetype = 'csv'
    districts_filetype = 'shp'


class BaseShpStationsShpDistrictsImporter(BaseStationsDistrictsImporter):
    """
    Stations in SHP format
    Districts in SHP format
    """

    stations_filetype = 'shp'
    districts_filetype = 'shp'


class BaseCsvStationsJsonDistrictsImporter(BaseStationsDistrictsImporter,
                                           CsvMixin):
    """
    Stations in CSV format
    Districts in GeoJSON format
    """

    stations_filetype = 'csv'
    districts_filetype = 'geojson'


class BaseCsvStationsKmlDistrictsImporter(BaseStationsDistrictsImporter,
                                          CsvMixin):
    """
    Stations in CSV format
    Districts in KML format
    """

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


class BaseScotlandSpatialHubImporter(BaseShpStationsShpDistrictsImporter,
                                     metaclass=abc.ABCMeta):

    """
    Data from the Scotland SpatialHub will be provided in a single
    dataset for the whole country. All importers consuming this data
    should extend BaseScotlandSpatialHubImporter.
    """

    srid = 27700
    districts_name = 'parl.2017-06-08/polling_districts_20170526.shp'
    stations_name = 'parl.2017-06-08/polling_places_20170526.shp'
    data_prefix = 'Scotland May 2017'
    run_in_series = True

    @property
    @abc.abstractmethod
    def council_name(self):
        pass

    @property
    def data_path(self):
        data_private = getattr(self, 'private', False)
        if data_private:
            path = getattr(
                settings,
                'PRIVATE_DATA_PATH',
                '../polling_station_data/')
        else:
            s3 = S3Wrapper()
            s3.fetch_data(self.data_prefix)
            path = s3.data_path
        return os.path.abspath(path)

    def get_base_folder_path(self):
        if getattr(self, 'local_files', True):
            if self.base_folder_path is None:
                path = os.path.join(self.data_path, self.data_prefix + '*')
                return glob.glob(path)[0]
        return self.base_folder_path

    def parse_string(self, text):
        try:
            return text.strip().decode('windows-1252')
        except AttributeError:
            return text.strip()

    def district_record_to_dict(self, record):
        council_name = self.parse_string(record[3])
        if council_name != self.council_name:
            return None

        code = self.parse_string(record[0])
        if not code:
            return None

        name = self.parse_string(record[1])
        if not name:
            name = code

        return {
            'internal_council_id': code,
            'name': name,
            'polling_station_id': code,
        }

    def station_record_to_dict(self, record):
        council_name = self.parse_string(record[3])
        if council_name != self.council_name:
            return None

        code = self.parse_string(record[1])
        if not code:
            return None

        address = self.parse_string(record[0])

        return {
            'internal_council_id': code,
            'postcode': '',
            'address': address,
        }


class BaseCsvStationsCsvAddressesImporter(BaseStationsAddressesImporter,
                                          CsvMixin):
    """
    Stations in CSV format
    Addresses in CSV format
    """

    stations_filetype = 'csv'
    addresses_filetype = 'csv'


class BaseShpStationsCsvAddressesImporter(BaseStationsAddressesImporter,
                                          CsvMixin):
    """
    Stations in SHP format
    Addresses in CSV format
    """

    stations_filetype = 'shp'
    addresses_filetype = 'csv'


class BaseGenericApiImporter(BaseStationsDistrictsImporter):
    srid = 4326
    districts_srid = 4326

    districts_name = None
    districts_url = None

    stations_name = None
    stations_url = None

    local_files = False

    def import_data(self):

        # Optional step for pre import tasks
        try:
            self.pre_import()
        except NotImplementedError:
            pass

        self.districts = DistrictSet()
        self.stations = StationSet()

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
            return self.get_data(self.districts_filetype, tmp.name)

    def get_stations(self):
        with tempfile.NamedTemporaryFile() as tmp:
            req = urllib.request.urlretrieve(self.stations_url, tmp.name)
            return self.get_data(self.stations_filetype, tmp.name)


class BaseApiKmlStationsKmlDistrictsImporter(BaseGenericApiImporter):
    """
    Stations in KML format
    Districts in KML format
    """

    stations_filetype = 'kml'
    districts_filetype = 'kml'


class BaseApiShpZipStationsShpZipDistrictsImporter(BaseGenericApiImporter):
    """
    Stations in Zipped SHP format
    Districts in Zipped SHP format
    """

    stations_filetype = 'shp.zip'
    districts_filetype = 'shp.zip'


class BaseApiCsvStationsShpZipDistrictsImporter(BaseGenericApiImporter,
                                                CsvMixin):
    """
    Stations in CSV format
    Districts in Zipped SHP format
    """

    stations_filetype = 'csv'
    districts_filetype = 'shp.zip'
