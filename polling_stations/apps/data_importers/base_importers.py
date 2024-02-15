"""
Defines the base importer classes to implement
"""
import abc
import contextlib
import datetime
import glob
import json
import logging
import os
import tempfile
import urllib.request
from typing import Callable, List

import rtree
from addressbase.models import UprnToCouncil
from councils.models import Council
from data_importers.contexthelpers import Dwellings
from data_importers.data_quality_report import (
    AddressReport,
    DataQualityReportBuilder,
    DistrictReport,
    StationReport,
)
from data_importers.data_types import AddressList, DistrictSet, StationSet
from data_importers.event_helpers import record_teardown_event
from data_importers.filehelpers import FileHelperFactory
from data_importers.loghelper import LogHelper
from data_importers.models import DataEvent, DataEventType, DataQuality
from data_importers.s3wrapper import S3Wrapper
from django.apps import apps
from django.conf import settings
from django.contrib.gis import geos
from django.contrib.gis.geos import GEOSException, GEOSGeometry, Point
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from file_uploads.models import File, Upload
from pollingstations.models import PollingDistrict, PollingStation


class CsvMixin:
    csv_encoding = "utf-8"
    csv_delimiter = ","

    def get_csv_options(self):
        return {"csv_encoding": self.csv_encoding, "csv_delimiter": self.csv_delimiter}


class ShpMixin:
    shp_encoding = "utf-8"

    def get_shp_options(self):
        return {"shp_encoding": self.shp_encoding}


class BaseBaseImporter:
    def post_import(self):
        pass

    def get_extra_reports(self):
        return []

    def teardown(self, council):
        pass


class BaseImporter(BaseBaseImporter, BaseCommand, metaclass=abc.ABCMeta):

    """
    Turn off auto system check for all apps
    We will manually run system checks only for the
    'data_importers' and 'pollingstations' apps
    """

    requires_system_checks = []

    srid = 27700
    council_id = None
    base_folder_path = None
    logger = None
    batch_size = None
    imports_districts = False
    use_postcode_centroids = False
    additional_report_councils = []

    def write_info(self, message):
        if self.verbosity > 0:
            self.stdout.write(message)

    def add_arguments(self, parser):
        parser.add_argument(
            "--nochecks",
            help="<Optional> Do not perform validation checks or display context information",
            action="store_true",
            required=False,
            default=False,
        )

        parser.add_argument(
            "-p",
            "--use-postcode-centroids",
            help="<optional> Use postcode centroids to derive a location for polling stations",
            action="store_true",
            required=False,
            default=False,
        )

        parser.add_argument(
            "-i",
            "--include-past-elections",
            help="<optional> Import data even if 'elections' property is missing or in the past",
            action="store_true",
            required=False,
            default=False,
        )

    def teardown(self, council):
        with transaction.atomic():
            super().teardown(council)
            PollingStation.objects.filter(council=council).delete()
            PollingDistrict.objects.filter(council=council).delete()
            UprnToCouncil.objects.filter(lad__in=council.identifiers).update(
                polling_station_id=""
            )
            record_teardown_event(self.council_id)

    def get_council(self, council_id):
        return Council.objects.get(pk=council_id)

    def get_data(self, filetype, filename):
        options = {}
        if hasattr(self, "get_csv_options"):
            options.update(self.get_csv_options())
        if hasattr(self, "get_shp_options"):
            options.update(self.get_shp_options())

        helper = FileHelperFactory.create(filetype, filename, options)
        return helper.get_features()

    def get_srid(self, type=None):
        if (
            hasattr(self, "districts_srid")
            and type == "districts"
            and self.districts_srid is not None
        ):
            return self.districts_srid
        return self.srid

    @abc.abstractmethod
    def import_data(self):
        pass

    def post_import(self):
        super().post_import()

    def get_extra_reports(self) -> List[Callable]:
        extra_reports: List = super().get_extra_reports()
        return extra_reports

    def report(self):
        # build report
        if hasattr(self, "csv_row_count"):
            report = DataQualityReportBuilder(
                self.council.pk,
                expecting_districts=self.imports_districts,
                csv_rows=self.csv_row_count,
                additional_report_councils=self.additional_report_councils,
            )
        else:
            report = DataQualityReportBuilder(
                self.council.pk,
                expecting_districts=self.imports_districts,
                additional_report_councils=self.additional_report_councils,
            )
        station_report = StationReport(self.council.pk, self.additional_report_councils)
        district_report = DistrictReport(self.council.pk)
        address_report = AddressReport(
            self.council.pk, additional_report_councils=self.additional_report_councils
        )

        report.build_report()

        for extra_report in self.get_extra_reports():
            report.report.add_row(extra_report(self, self.council))

        # save a static copy in the DB that we can serve up on the website
        record = DataQuality.objects.get_or_create(council_id=self.council.pk)
        record[0].num_stations = station_report.get_stations_imported()
        record[0].num_districts = district_report.get_districts_imported()
        record[0].num_addresses = address_report.get_addresses_with_station_id()
        record[0].report = report.generate_string_report()
        record[0].save()

    @property
    def data_path(self):
        if getattr(settings, "PRIVATE_DATA_PATH", None):
            path = settings.PRIVATE_DATA_PATH
        else:
            s3 = S3Wrapper()
            s3.fetch_data_by_council(self.council_id)
            path = s3.data_path
        return os.path.abspath(path)

    def get_base_folder_path(self):
        if getattr(self, "local_files", True) and self.base_folder_path is None:
            path = os.path.join(self.data_path, self.council_id)
            return glob.glob(path)[0]
        return self.base_folder_path

    def covers_current_elections(self):
        """
        Checks whether the import script is covering future elections
        depends on setting the 'elections' attribute
        If 'elections' attribute is unset returns False
        """
        if not hasattr(self, "elections"):
            return False
        for date_str in self.elections:
            try:
                election_date = datetime.date.fromisoformat(date_str)
                if election_date >= datetime.date.today():
                    return True
            except ValueError:
                self.logger.log_message(
                    logging.WARNING,
                    f"{date_str} can't be interpreted as an ISO date format."
                    f"Can't tell if it covers current election",
                )
        return False

    @abc.abstractmethod
    def get_upload(self):
        pass

    def record_import_event(self):
        DataEvent.objects.create(
            council=self.get_council(self.council_id),
            upload=self.get_upload(),
            event_type=DataEventType.IMPORT,
            election_dates=self.election_dates,
        )

    @property
    def election_dates(self):
        if hasattr(self, "elections"):
            return [
                datetime.datetime.strptime(date_string, "%Y-%m-%d")
                for date_string in self.elections
            ]
        return []

    def handle(self, *args, **kwargs):
        """
        Manually run system checks for the
        'data_importers' and 'pollingstations' apps
        Management commands can ignore checks that only apply to
        the apps supporting the website part of the project
        """
        self.check(
            [
                apps.get_app_config("data_importers"),
                apps.get_app_config("pollingstations"),
            ]
        )

        self.verbosity = kwargs.get("verbosity")
        self.logger = LogHelper(self.verbosity)
        self.validation_checks = not (kwargs.get("nochecks"))
        self.allow_station_point_from_postcode = kwargs.get("use_postcode_centroids")

        if self.council_id is None:
            self.council_id = args[0]

        self.council = self.get_council(self.council_id)

        if (
            not kwargs.get("include_past_elections")
            and not self.covers_current_elections()
        ):
            if hasattr(self, "elections"):
                raise CommandError(
                    f"'elections' attribute in the import script for {self.council.name} only has dates in the past\n"
                    f"{self.elections=}"
                    "Consider passing the '--include-past-elections' flag"
                )

            raise CommandError(
                f"Import script for {self.council.name} does not have an elections attribute"
            )

        self.write_info("Importing data for %s..." % self.council.name)

        # Delete old data for this council
        self.teardown(self.council)

        self.base_folder_path = self.get_base_folder_path()

        with transaction.atomic():
            self.import_data()
            self.record_import_event()
        self.council.update_all_station_visibilities_from_events(self.election_dates)

        # Optional step for post import tasks
        self.post_import()

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
        if station_record["location"]:
            self.check_in_council_bounds(station_record)
            self.check_duplicate_location(station_record)

    def check_duplicate_location(self, station_record):
        stations_with_location_and_different_postcode = [
            s
            for s in self.stations.elements
            if s.location and (s.postcode != station_record["postcode"])
        ]

        if not stations_with_location_and_different_postcode:
            return

        srids = [
            GEOSGeometry(s.location).srid
            for s in stations_with_location_and_different_postcode
        ]
        srid_to_use = max(srids, key=srids.count)

        if srid_to_use == 4326:
            threshold = 0.0001
        if srid_to_use == 27700:
            threshold = 10

        station_index = rtree.index.Index()
        for i, station in enumerate(stations_with_location_and_different_postcode):
            geom = GEOSGeometry(station.location).transform(srid_to_use, clone=True)
            station_index.insert(i, (geom.x, geom.y, geom.x, geom.y))

        record_geom = station_record["location"].transform(srid_to_use, clone=True)
        nearest_ids = list(
            station_index.intersection(
                (
                    record_geom.x - threshold,
                    record_geom.y - threshold,
                    record_geom.x + threshold,
                    record_geom.y + threshold,
                ),
                1,
            )
        )

        if not nearest_ids:
            return

        for i in nearest_ids:
            station = stations_with_location_and_different_postcode[i.id]

            def get_name(address):
                return " ".join(address.split("\n")[:2])

            self.logger.log_message(
                logging.WARNING,
                f"Polling stations '{get_name(station_record['address'])}' and "
                f"'{get_name(station.address)}' "
                "are at approximately the same location, but have different postcodes:\n"
                f"qgis filter exp: \"internal_council_id\" IN ('{station_record['internal_council_id']}','{station.internal_council_id}')",  # qgis filter expression
            )

    def check_in_council_bounds(self, station_record):
        station_name = station_record["address"].split("\n")[0]
        try:
            council = Council.objects.get(
                geography__geography__covers=station_record["location"]
            )
            if self.council_id != council.council_id:
                self.logger.log_message(
                    logging.WARNING,
                    f"Polling station {station_name} ({station_record['internal_council_id']}) is in {council.name} ({council.council_id}) "
                    f"but target council is {self.council.name} ({self.council.council_id}) - manual check recommended\n",
                )
        except Council.DoesNotExist:
            self.logger.log_message(
                logging.WARNING,
                "Polling station %s (%s) is not covered by any council area - manual check recommended\n",
                variable=(
                    station_name,
                    station_record["internal_council_id"],
                ),
            )

    def import_polling_stations(self):
        stations = self.get_stations()
        if not isinstance(self, BaseAddressesImporter):
            self.write_info(
                "Stations: Found %i features in input file" % (len(stations))
            )
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
                self.logger.log_message(
                    logging.INFO,
                    "Polling station added to set:\n%s",
                    variable=station,
                    pretty=True,
                )
                seen.add(station_hash)
            except NotImplementedError:
                pass

            if self.stations_filetype in ["shp", "shp.zip"]:
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
                    logging.INFO,
                    "station_record_to_dict() returned list with input:\n%s",
                    variable=record,
                    pretty=True,
                )
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
                        variable=record,
                        pretty=True,
                    )
                    continue

                if "council" not in station_record:
                    station_record["council"] = self.council

                """
                If the file type is shp, we can usually derive 'location'
                automatically, but we can return it if necessary.
                For other file types, we must return the key
                'location' from station_record_to_dict()
                """
                if (
                    self.stations_filetype in ["shp", "shp.zip"]
                    and "location" not in station_record
                ):
                    if len(station.shape.points) == 1:
                        # we've got a point
                        station_record["location"] = Point(
                            *station.shape.points[0], srid=self.get_srid()
                        )
                    else:
                        # its a polygon: simplify it to a centroid and warn
                        self.logger.log_message(
                            logging.WARNING,
                            "Implicitly converting station geometry to point",
                        )
                        geojson = json.dumps(station.shape.__geo_interface__)
                        poly = self.clean_poly(GEOSGeometry(geojson))
                        poly.srid = self.get_srid()
                        station_record["location"] = poly.centroid

                if self.validation_checks:
                    self.check_station_point(station_record)
                self.add_polling_station(station_record)

    def add_polling_station(self, station_info):
        self.stations.add(station_info)


class BaseDistrictsImporter(BaseImporter, metaclass=abc.ABCMeta):
    imports_districts = True

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

    def get_upload(self):
        return None

    def get_districts(self):
        districts_file = os.path.join(self.base_folder_path, self.districts_name)
        return self.get_data(self.districts_filetype, districts_file)

    def clean_poly(self, poly):
        if isinstance(poly, geos.Polygon):
            return geos.MultiPolygon(poly, srid=self.get_srid("districts"))
        return poly

    def strip_z_values(self, geojson):
        districts = json.loads(geojson)
        districts["type"] = "Polygon"
        for points in districts["coordinates"][0][0]:
            if len(points) == 3:
                points.pop()
        districts["coordinates"] = districts["coordinates"][0]
        return json.dumps(districts)

    @abc.abstractmethod
    def district_record_to_dict(self, record):
        pass

    def check_district_overlap(self, district_record):
        if self.council.geography.geography.contains(district_record["area"]):
            self.logger.log_message(
                logging.INFO,
                "District %s is fully contained by target local auth",
                variable=district_record["internal_council_id"],
            )
            return 100

        try:
            intersection = self.council.geography.geography.intersection(
                district_record["area"].transform(4326, clone=True)
            )
            district_area = district_record["area"].transform(27700, clone=True).area
            intersection_area = intersection.transform(27700, clone=True).area
        except GEOSException as e:
            self.logger.log_message(logging.ERROR, str(e))
            return None

        overlap_percentage = (intersection_area / district_area) * 100

        # meh - close enough
        level = logging.INFO if overlap_percentage > 99 else logging.WARNING

        self.logger.log_message(
            level,
            "District {0} is {1:.2f}% contained by target local auth".format(
                district_record["internal_council_id"], overlap_percentage
            ),
        )

        return overlap_percentage

    def import_polling_districts(self):
        districts = self.get_districts()
        self.write_info("Districts: Found %i features in input file" % (len(districts)))
        for district in districts:
            if self.districts_filetype in ["shp", "shp.zip"]:
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
                    variable=district,
                    pretty=True,
                )
                continue

            if "council" not in district_info:
                district_info["council"] = self.council

            """
            If the file type is shp or geojson, we can usually derive
            'area' automatically, but we can return it if necessary.
            For other file types, we must return the key
            'area' from address_record_to_dict()
            """
            if self.districts_filetype in ["shp", "shp.zip"]:
                geojson = json.dumps(district.shape.__geo_interface__)
            if self.districts_filetype == "geojson":
                geojson = json.dumps(district["geometry"])
            if "area" not in district_info and (
                self.districts_filetype in ["shp", "shp.zip", "geojson"]
            ):
                poly = self.clean_poly(GEOSGeometry(geojson))
                poly.srid = self.get_srid("districts")
                district_info["area"] = poly

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

    @abc.abstractmethod
    def address_record_to_dict(self, record):
        pass

    def get_upload(self):
        try:
            upload = File.objects.get(
                key=f"{self.council_id}/{self.addresses_name}"
            ).upload
        except File.DoesNotExist:
            return None
        except Upload.DoesNotExist:
            return None
        return upload

    def write_context_data(self):
        dwellings = Dwellings()
        self.write_info("----------------------------------")
        self.write_info("Contextual Data:")
        self.write_info(
            "Total UPRNs in AddressBase: {:,}".format(
                dwellings.from_addressbase(self.council.geography.geography)
            )
        )
        self.write_info(
            "Total Dwellings from 2021 Census: {:,}".format(
                dwellings.from_census(self.council.geography.gss)
            )
        )
        self.write_info("----------------------------------")

    def import_residential_addresses(self):
        if self.validation_checks:
            self.write_context_data()
        addresses = self.get_addresses()
        self.csv_row_count = len(addresses)
        self.write_info(
            "Addresses: Found {:,} rows in input file".format(self.csv_row_count)
        )
        for address in addresses:
            address_info = self.address_record_to_dict(address)

            if address_info is None:
                self.logger.log_message(
                    logging.INFO,
                    "address_record_to_dict() returned None with input:\n%s",
                    variable=address,
                    pretty=True,
                )
                continue

            self.add_residential_address(address_info)

        element_set = {frozenset(d.items()) for d in self.addresses.elements}
        self.write_info(
            "Addresses: Found {:,} unique records after converting to dicts. Removing duplicates".format(
                len(element_set)
            )
        )
        self.addresses.elements = [dict(s) for s in element_set]
        self.csv_row_count = len(self.addresses.elements)
        self.write_info(
            "Addresses: Found {:,} distinct records in input file".format(
                self.csv_row_count
            )
        )
        self.write_info("----------------------------------")  #

    def add_residential_address(self, address_info):
        if "council" not in address_info:
            address_info["council"] = self.council

        if "uprn" not in address_info:
            address_info["uprn"] = ""
        else:
            # UPRNs less than 12 characters long may be left padded with zeros
            # Making sure uprns in our addresslist are not left padded will help with matching them
            # and catching duplicates.
            address_info["uprn"] = str(address_info["uprn"]).lstrip("0")

        self.addresses.append(address_info)


class BaseStationsDistrictsImporter(BaseStationsImporter, BaseDistrictsImporter):
    def pre_import(self):
        raise NotImplementedError

    @property
    def districts_have_station_ids(self):
        """
        Check that we've called self.import_polling_{districts,stations}
        Don't raise an exception though, because we might still want to
        import just stations or districts for debugging - i.e. to see them
        in qgis/the db. However if we don't also have the other half we
        won't be able to update the UprnToCouncil table.
        """
        if len(self.districts.elements) < 1:
            self.logger.log_message(
                logging.WARNING, "No district records added to self.districts"
            )
        if len(self.stations.elements) < 1:
            self.logger.log_message(
                logging.WARNING, "No station records added to self.stations"
            )

        district_ids = {
            e.internal_council_id
            for e in self.districts.elements
            if e.internal_council_id != ""
        }
        station_ids_from_districts = {
            e.polling_station_id
            for e in self.districts.elements
            if e.polling_station_id != ""
        }
        station_ids = {
            e.internal_council_id
            for e in self.stations.elements
            if e.internal_council_id != ""
        }
        district_ids_from_stations = {
            e.polling_district_id
            for e in self.stations.elements
            if e.polling_district_id != ""
        }

        def get_missing(set_a, set_b):
            return set_a - set_b

        if station_ids_from_districts:
            self.write_info("Districts have station ids attached")
            missing_ids = get_missing(station_ids_from_districts, station_ids)
            for station_id in missing_ids:
                self.logger.log_message(
                    logging.WARNING,
                    "Station id: %s attached to a district but not found in stations",
                    variable=station_id,
                )

            for station_id in get_missing(station_ids, station_ids_from_districts):
                self.logger.log_message(
                    logging.WARNING,
                    "Station id: %s found in stations but not attached to any station",
                    variable=station_id,
                )
            return True

        if district_ids_from_stations:
            self.write_info("Stations have district ids attached")

            for district_id in get_missing(district_ids_from_stations, district_ids):
                self.logger.log_message(
                    logging.WARNING,
                    "District id: %s attached to a station but not found in districts",
                    variable=district_id,
                )

            for district_id in get_missing(district_ids, district_ids_from_stations):
                self.logger.log_message(
                    logging.WARNING,
                    "District id: %s found in districts but not attached to any station",
                    variable=district_id,
                )
            return False
        return None

    def import_data(self):
        # Optional step for pre import tasks
        with contextlib.suppress(NotImplementedError):
            self.pre_import()

        self.stations = StationSet()
        self.districts = DistrictSet()
        self.import_polling_districts()
        self.import_polling_stations()
        self.districts.save()
        self.stations.save()
        self.districts.update_uprn_to_council_model(self.districts_have_station_ids)


class BaseStationsAddressesImporter(BaseStationsImporter, BaseAddressesImporter):
    def pre_import(self):
        raise NotImplementedError

    def import_data(self):
        # Optional step for pre import tasks
        with contextlib.suppress(NotImplementedError):
            self.pre_import()

        self.stations = StationSet()
        self.addresses = AddressList(self.logger)
        self.import_residential_addresses()
        self.import_polling_stations()
        self.addresses.check_records()
        self.addresses.update_uprn_to_council_model()
        self.stations.save()


class BaseCsvStationsShpDistrictsImporter(
    BaseStationsDistrictsImporter, CsvMixin, ShpMixin
):
    """
    Stations in CSV format
    Districts in SHP format
    """

    stations_filetype = "csv"
    districts_filetype = "shp"


class BaseShpStationsShpDistrictsImporter(BaseStationsDistrictsImporter, ShpMixin):
    """
    Stations in SHP format
    Districts in SHP format
    """

    stations_filetype = "shp"
    districts_filetype = "shp"


class BaseCsvStationsJsonDistrictsImporter(BaseStationsDistrictsImporter, CsvMixin):
    """
    Stations in CSV format
    Districts in GeoJSON format
    """

    stations_filetype = "csv"
    districts_filetype = "geojson"


class BaseCsvStationsKmlDistrictsImporter(BaseStationsDistrictsImporter, CsvMixin):
    """
    Stations in CSV format
    Districts in KML format
    """

    districts_srid = 4326
    stations_filetype = "csv"
    districts_filetype = "kml"

    # this is mainly here for legacy compatibility
    # mostly we should override this
    def district_record_to_dict(self, record):
        geojson = self.strip_z_values(record.geom.geojson)
        poly = self.clean_poly(GEOSGeometry(geojson, srid=self.get_srid("districts")))
        return {
            "internal_council_id": record["Name"].value,
            "name": record["Name"].value,
            "area": poly,
        }


class BaseScotlandSpatialHubImporter(
    BaseShpStationsShpDistrictsImporter, metaclass=abc.ABCMeta
):

    """
    Data from the Scotland SpatialHub will be provided in a single
    dataset for the whole country. All importers consuming this data
    should extend BaseScotlandSpatialHubImporter.
    """

    srid = 27700
    districts_name = "parl.2019-12-12/Version 2/Polling-Districts/pub_poldi.shp"
    stations_name = "parl.2019-12-12/Version 2/Polling-Places/pub_polpl.shp"
    data_prefix = "Scotland-Dec 2019"
    shp_encoding = "latin-1"

    @property
    @abc.abstractmethod
    def council_name(self):
        pass

    @property
    def data_path(self):
        if getattr(settings, "PRIVATE_DATA_PATH", None):
            path = settings.PRIVATE_DATA_PATH
        else:
            s3 = S3Wrapper()
            s3.fetch_data(self.data_prefix)
            path = s3.data_path
        return os.path.abspath(path)

    def get_base_folder_path(self):
        if getattr(self, "local_files", True) and self.base_folder_path is None:
            path = os.path.join(self.data_path, self.data_prefix + "*")
            return glob.glob(path)[0]
        return self.base_folder_path

    def parse_string(self, text):
        return text.strip().strip("\x00")

    def district_record_to_dict(self, record):
        council_name = self.parse_string(record[2])
        if council_name != self.council_name:
            return None

        code = self.parse_string(record[0])
        if not code:
            return None

        name = self.parse_string(record[1])
        if not name:
            name = code

        return {"internal_council_id": code, "name": name, "polling_station_id": code}

    def station_record_to_dict(self, record):
        council_name = self.parse_string(record[2])
        if council_name != self.council_name:
            return None

        code = self.parse_string(record[0])
        if not code:
            return None

        address = self.parse_string(record[3])

        return {"internal_council_id": code, "postcode": "", "address": address}


class BaseCsvStationsCsvAddressesImporter(BaseStationsAddressesImporter, CsvMixin):
    """
    Stations in CSV format
    Addresses in CSV format
    """

    stations_filetype = "csv"
    addresses_filetype = "csv"


class BaseShpStationsCsvAddressesImporter(
    BaseStationsAddressesImporter, CsvMixin, ShpMixin
):
    """
    Stations in SHP format
    Addresses in CSV format
    """

    stations_filetype = "shp"
    addresses_filetype = "csv"


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
        with contextlib.suppress(NotImplementedError):
            self.pre_import()

        self.districts = DistrictSet()
        self.stations = StationSet()

        # deal with 'stations only' or 'districts only' data
        if self.districts_url is not None:
            self.import_polling_districts()
        if self.stations_url is not None:
            self.import_polling_stations()

        self.districts.save()
        self.stations.save()
        self.districts.update_uprn_to_council_model(self.districts_have_station_ids)

    def get_districts(self):
        with tempfile.NamedTemporaryFile() as tmp:
            urllib.request.urlretrieve(self.districts_url, tmp.name)
            return self.get_data(self.districts_filetype, tmp.name)

    def get_stations(self):
        with tempfile.NamedTemporaryFile() as tmp:
            urllib.request.urlretrieve(self.stations_url, tmp.name)
            return self.get_data(self.stations_filetype, tmp.name)

    def get_upload(self):
        return None


class BaseApiKmlStationsKmlDistrictsImporter(BaseGenericApiImporter):
    """
    Stations in KML format
    Districts in KML format
    """

    stations_filetype = "kml"
    districts_filetype = "kml"


class BaseApiShpZipStationsShpZipDistrictsImporter(BaseGenericApiImporter, ShpMixin):
    """
    Stations in Zipped SHP format
    Districts in Zipped SHP format
    """

    stations_filetype = "shp.zip"
    districts_filetype = "shp.zip"


class BaseApiCsvStationsShpZipDistrictsImporter(
    BaseGenericApiImporter, CsvMixin, ShpMixin
):
    """
    Stations in CSV format
    Districts in Zipped SHP format
    """

    stations_filetype = "csv"
    districts_filetype = "shp.zip"
