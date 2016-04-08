from django.db import connection
from django.db.models import Q
from pollingstations.models import PollingStation, PollingDistrict, ResidentialAddress


# define some methods we can use to print coloured console output
class OutputFormatter:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

    @staticmethod
    def print_ok(text):
        print(OutputFormatter.OKGREEN + text + OutputFormatter.ENDC)

    @staticmethod
    def print_warning(text):
        print(OutputFormatter.WARNING + text + OutputFormatter.ENDC)

    @staticmethod
    def print_bold(text):
        print(OutputFormatter.BOLD + text + OutputFormatter.ENDC)

    @staticmethod
    def print_ok_bold(text):
        print(OutputFormatter.OKGREEN + OutputFormatter.BOLD + text + OutputFormatter.ENDC)


# data quality stats for polling stations
class StationReport():

    council_id = None
    counts = {
        '0': 0,
        '1': 0,
        '>1': 0
    }

    def __init__(self, council_id):
        self.council_id = council_id
        self.generate_counts()

    def get_stations_imported(self):
        return PollingStation.objects.filter(
            council_id=self.council_id
        ).count()

    def get_stations_with_district_id(self):
        return PollingStation.objects.filter(
            council_id=self.council_id,
            polling_district_id__isnull=False
        ).exclude(polling_district_id='').count()

    def get_stations_without_district_id(self):
        return PollingStation.objects.filter(
            Q(polling_district_id__isnull=True) | Q(polling_district_id=''),
            council_id=self.council_id
        ).count()

    def get_stations_with_valid_district_id_ref(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM pollingstations_pollingstation
            WHERE polling_district_id IN
                (SELECT internal_council_id FROM pollingstations_pollingdistrict
                WHERE council_id=%s)
            AND council_id=%s
            AND polling_district_id != ''
            AND polling_district_id IS NOT NULL;
        """,
        [self.council_id, self.council_id])
        results = cursor.fetchall()
        return results[0][0]

    def get_stations_with_invalid_district_id_ref(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM pollingstations_pollingstation
            WHERE polling_district_id NOT IN
                (SELECT internal_council_id FROM pollingstations_pollingdistrict
                WHERE council_id=%s)
            AND council_id=%s
            AND polling_district_id != ''
            AND polling_district_id IS NOT NULL;
        """,
        [self.council_id, self.council_id])
        results = cursor.fetchall()
        return results[0][0]

    def get_stations_with_point(self):
        return PollingStation.objects.filter(
            council_id=self.council_id,
            location__isnull=False
        ).count()

    def get_stations_without_point(self):
        return PollingStation.objects.filter(
            council_id=self.council_id,
            location__isnull=True
        ).count()

    def get_stations_with_address(self):
        return PollingStation.objects.filter(
            council_id=self.council_id,
            address__isnull=False
        ).exclude(address='').count()

    def get_stations_without_address(self):
        return PollingStation.objects.filter(
            Q(address__isnull=True) | Q(address=''),
            council_id=self.council_id
        ).count()

    def generate_counts(self):
        stations = PollingStation.objects.filter(
            council_id=self.council_id
        )
        counts = []
        for station in stations:
            if station.location is not None:
                counts.append(
                    PollingDistrict.objects.filter(
                        area__contains=station.location
                    ).count()
                )
        for count in counts:
            if count == 0:
                self.counts['0'] = self.counts['0'] + 1
            elif count == 1:
                self.counts['1'] = self.counts['1'] + 1
            else:
                self.counts['>1'] = self.counts['>1'] + 1

    def get_stations_in_zero_districts(self):
        return self.counts['0']

    def get_stations_in_one_districts(self):
        return self.counts['1']

    def get_stations_in_more_districts(self):
        return self.counts['>1']


# data quality stats for polling districts
class DistrictReport():

    council_id = None
    counts = {
        '0': 0,
        '1': 0,
        '>1': 0
    }

    def __init__(self, council_id):
        self.council_id = council_id
        self.generate_counts()

    def get_districts_imported(self):
        return PollingDistrict.objects.filter(
            council_id=self.council_id
        ).count()

    def get_districts_with_station_id(self):
        return PollingDistrict.objects.filter(
            council_id=self.council_id,
            polling_station_id__isnull=False
        ).exclude(polling_station_id='').count()

    def get_districts_without_station_id(self):
        return PollingDistrict.objects.filter(
            Q(polling_station_id__isnull=True) | Q(polling_station_id=''),
            council_id=self.council_id
        ).count()

    def get_districts_with_valid_station_id_ref(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM pollingstations_pollingdistrict
            WHERE polling_station_id IN
                (SELECT internal_council_id FROM pollingstations_pollingstation
                WHERE council_id=%s)
            AND council_id=%s
            AND polling_station_id != ''
            AND polling_station_id IS NOT NULL;
        """,
        [self.council_id, self.council_id])
        results = cursor.fetchall()
        return results[0][0]

    def get_districts_with_invalid_station_id_ref(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM pollingstations_pollingdistrict
            WHERE polling_station_id NOT IN
                (SELECT internal_council_id FROM pollingstations_pollingstation
                WHERE council_id=%s)
            AND council_id=%s
            AND polling_station_id != ''
            AND polling_station_id IS NOT NULL;
        """,
        [self.council_id, self.council_id])
        results = cursor.fetchall()
        return results[0][0]

    def generate_counts(self):
        districts = PollingDistrict.objects.filter(
            council_id=self.council_id
        )
        counts = []
        for district in districts:
            if district.area is not None:
                counts.append(
                    PollingStation.objects.filter(
                        location__within=district.area
                    ).count()
                )
        for count in counts:
            if count == 0:
                self.counts['0'] = self.counts['0'] + 1
            elif count == 1:
                self.counts['1'] = self.counts['1'] + 1
            else:
                self.counts['>1'] = self.counts['>1'] + 1

    def get_districts_containing_zero_stations(self):
        return self.counts['0']

    def get_districts_containing_one_stations(self):
        return self.counts['1']

    def get_districts_containing_more_stations(self):
        return self.counts['>1']


# data quality stats for residential addresses
class ResidentialAddressReport():

    council_id = None

    def __init__(self, council_id):
        self.council_id = council_id

    def get_addresses_imported(self):
        return ResidentialAddress.objects.filter(
            council_id=self.council_id
        ).count()

    def get_addresses_with_station_id(self):
        return ResidentialAddress.objects.filter(
            council_id=self.council_id,
            polling_station_id__isnull=False
        ).exclude(polling_station_id='').count()

    def get_addresses_without_station_id(self):
        return ResidentialAddress.objects.filter(
            Q(polling_station_id__isnull=True) | Q(polling_station_id=''),
            council_id=self.council_id
        ).count()

    def get_addresses_with_valid_station_id_ref(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM pollingstations_residentialaddress
            WHERE polling_station_id IN
                (SELECT internal_council_id FROM pollingstations_pollingstation
                WHERE council_id=%s)
            AND council_id=%s
            AND polling_station_id != ''
            AND polling_station_id IS NOT NULL;
        """,
        [self.council_id, self.council_id])
        results = cursor.fetchall()
        return results[0][0]

    def get_addresses_with_invalid_station_id_ref(self):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM pollingstations_residentialaddress
            WHERE polling_station_id NOT IN
                (SELECT internal_council_id FROM pollingstations_pollingstation
                WHERE council_id=%s)
            AND council_id=%s
            AND polling_station_id != ''
            AND polling_station_id IS NOT NULL;
        """,
        [self.council_id, self.council_id])
        results = cursor.fetchall()
        return results[0][0]


# generate all the stats and output to console
class DataQualityReport():

    council_id = None

    def __init__(self, council_id):
        self.council_id = council_id

    def output_header(self):
        print("==================================")
        OutputFormatter.print_bold("        DATA QUALITY REPORT")
        print("==================================\n")

    def output_station_report(self):
        stations_report = StationReport(self.council_id)

        stations_imported = stations_report.get_stations_imported()
        if stations_imported > 0:
            OutputFormatter.print_bold("STATIONS IMPORTED                : %i" % (stations_imported))
            print("----------------------------------")
            district_ids = stations_report.get_stations_with_district_id()
            if district_ids > 0:
                OutputFormatter.print_ok_bold(" - with district id              : %i" % (district_ids))
                OutputFormatter.print_ok("   - valid district id refs      : %i" % (stations_report.get_stations_with_valid_district_id_ref()))
                OutputFormatter.print_warning("   - invalid district id refs    : %i" % (stations_report.get_stations_with_invalid_district_id_ref()))
            else:
                OutputFormatter.print_ok(" - with district id              : %i" % (district_ids))
            OutputFormatter.print_warning(" - without district id           : %i" % (stations_report.get_stations_without_district_id()))
            OutputFormatter.print_ok(" - with point                    : %i" % (stations_report.get_stations_with_point()))
            OutputFormatter.print_warning(" - without point                 : %i" % (stations_report.get_stations_without_point()))
            OutputFormatter.print_ok(" - with address                  : %i" % (stations_report.get_stations_with_address()))
            OutputFormatter.print_warning(" - without address               : %i" % (stations_report.get_stations_without_address()))
            print("----------------------------------")
            OutputFormatter.print_bold("POLYGON LOOKUPS")
            OutputFormatter.print_warning("Stations in 0 districts          : %i" % (stations_report.get_stations_in_zero_districts()))
            OutputFormatter.print_ok("Stations in 1 districts          : %i" % (stations_report.get_stations_in_one_districts()))
            OutputFormatter.print_warning("Stations in >1 districts         : %i" % (stations_report.get_stations_in_more_districts()))
            print("\n")

    def output_district_report(self):
        districts_report = DistrictReport(self.council_id)

        districts_imported = districts_report.get_districts_imported()
        if districts_imported > 0:
            OutputFormatter.print_bold("DISTRICTS IMPORTED               : %i" % (districts_imported))
            print("----------------------------------")
            station_ids = districts_report.get_districts_with_station_id()
            if station_ids > 0:
                OutputFormatter.print_ok_bold(" - with station id               : %i" % (station_ids))
                OutputFormatter.print_ok("   - valid station id refs       : %i" % (districts_report.get_districts_with_valid_station_id_ref()))
                OutputFormatter.print_warning("   - invalid station id refs     : %i" % (districts_report.get_districts_with_invalid_station_id_ref()))
            else:
                OutputFormatter.print_ok(" - with station id               : %i" % (station_ids))
            OutputFormatter.print_warning(" - without station id            : %i" % (districts_report.get_districts_without_station_id()))
            print("----------------------------------")
            OutputFormatter.print_bold("POLYGON LOOKUPS")
            OutputFormatter.print_warning("Districts containing 0 stations  : %i" % (districts_report.get_districts_containing_zero_stations()))
            OutputFormatter.print_ok("Districts containing 1 stations  : %i" % (districts_report.get_districts_containing_one_stations()))
            OutputFormatter.print_warning("Districts containing >1 stations : %i" % (districts_report.get_districts_containing_more_stations()))
            print("\n")

    def output_residential_address_report(self):
        address_report = ResidentialAddressReport(self.council_id)

        addresses_imported = address_report.get_addresses_imported()
        if addresses_imported > 0:
            OutputFormatter.print_bold("ADDRESSES IMPORTED               : %i" % (addresses_imported))
            print("----------------------------------")
            station_ids = address_report.get_addresses_with_station_id()
            if station_ids > 0:
                OutputFormatter.print_ok_bold(" - with station id               : %i" % (station_ids))
                OutputFormatter.print_ok("   - valid station id refs       : %i" % (address_report.get_addresses_with_valid_station_id_ref()))
                OutputFormatter.print_warning("   - invalid station id refs     : %i" % (address_report.get_addresses_with_invalid_station_id_ref()))
            else:
                OutputFormatter.print_ok(" - with station id               : %i" % (station_ids))
            OutputFormatter.print_warning(" - without station id            : %i" % (address_report.get_addresses_without_station_id()))
            print("\n")

    def output_report(self):
        self.output_header()
        self.output_district_report()
        self.output_station_report()
        self.output_residential_address_report()
