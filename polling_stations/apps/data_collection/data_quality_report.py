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
        self.counts = {
            '0': 0,
            '1': 0,
            '>1': 0
        }
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
        self.counts = {
            '0': 0,
            '1': 0,
            '>1': 0
        }
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


# generate all the stats
class DataQualityReportBuilder():

    council_id = None
    report = []

    def __init__(self, council_id):
        self.council_id = council_id

    def build_header(self):
        self.report.append({ 'style': None,
            'text': "=================================="
        })
        self.report.append({ 'style': 'bold',
            'text': "        DATA QUALITY REPORT"
        })
        self.report.append({ 'style': None,
            'text': "==================================\n"
        })

    def build_station_report(self):
        stations_report = StationReport(self.council_id)

        stations_imported = stations_report.get_stations_imported()
        if stations_imported > 0:
            self.report.append({ 'style': 'bold',
                'text': "STATIONS IMPORTED                : %i" % (stations_imported)
            })
            self.report.append({ 'style': None,
                'text': "----------------------------------"
            })

            district_ids = stations_report.get_stations_with_district_id()
            if district_ids > 0:
                self.report.append({ 'style': 'ok_bold',
                    'text': " - with district id              : %i" % (district_ids)
                })
                self.report.append({ 'style': 'ok',
                    'text': "   - valid district id refs      : %i" % (stations_report.get_stations_with_valid_district_id_ref())
                })
                self.report.append({ 'style': 'warning',
                    'text': "   - invalid district id refs    : %i" % (stations_report.get_stations_with_invalid_district_id_ref())
                })
            else:
                self.report.append({ 'style': 'ok',
                    'text': " - with district id              : %i" % (district_ids)
                })

            self.report.append({ 'style': 'warning',
                'text': " - without district id           : %i" % (stations_report.get_stations_without_district_id())
            })
            self.report.append({ 'style': 'ok',
                'text': " - with point                    : %i" % (stations_report.get_stations_with_point())
            })
            self.report.append({ 'style': 'warning',
                'text': " - without point                 : %i" % (stations_report.get_stations_without_point())
            })
            self.report.append({ 'style': 'ok',
                'text': " - with address                  : %i" % (stations_report.get_stations_with_address())
            })
            self.report.append({ 'style': 'warning',
                'text': " - without address               : %i" % (stations_report.get_stations_without_address())
            })
            self.report.append({ 'style': None,
                'text': "----------------------------------"
            })
            self.report.append({ 'style': 'bold',
                'text': "POLYGON LOOKUPS"
            })
            self.report.append({ 'style': 'warning',
                'text': "Stations in 0 districts          : %i" % (stations_report.get_stations_in_zero_districts())
            })
            self.report.append({ 'style': 'ok',
                'text': "Stations in 1 districts          : %i" % (stations_report.get_stations_in_one_districts())
            })
            self.report.append({ 'style': 'warning',
                'text': "Stations in >1 districts         : %i" % (stations_report.get_stations_in_more_districts())
            })
            self.report.append({ 'style': None,
                'text': "\n"
            })

    def build_district_report(self):
        districts_report = DistrictReport(self.council_id)

        districts_imported = districts_report.get_districts_imported()
        if districts_imported > 0:
            self.report.append({ 'style': 'bold',
                'text': "DISTRICTS IMPORTED               : %i" % (districts_imported)
            })
            self.report.append({ 'style': None,
                'text': "----------------------------------"
            })

            station_ids = districts_report.get_districts_with_station_id()
            if station_ids > 0:
                self.report.append({ 'style': 'ok_bold',
                    'text': " - with station id               : %i" % (station_ids)
                })
                self.report.append({ 'style': 'ok',
                    'text': "   - valid station id refs       : %i" % (districts_report.get_districts_with_valid_station_id_ref())
                })
                self.report.append({ 'style': 'warning',
                    'text': "   - invalid station id refs     : %i" % (districts_report.get_districts_with_invalid_station_id_ref())
                })
            else:
                self.report.append({ 'style': 'ok',
                    'text': " - with station id               : %i" % (station_ids)
                })

            self.report.append({ 'style': 'warning',
                'text': " - without station id            : %i" % (districts_report.get_districts_without_station_id())
            })
            self.report.append({ 'style': None,
                'text': "----------------------------------"
            })
            self.report.append({ 'style': 'bold',
                'text': "POLYGON LOOKUPS"
            })
            self.report.append({ 'style': 'warning',
                'text': "Districts containing 0 stations  : %i" % (districts_report.get_districts_containing_zero_stations())
            })
            self.report.append({ 'style': 'ok',
                'text': "Districts containing 1 stations  : %i" % (districts_report.get_districts_containing_one_stations())
            })
            self.report.append({ 'style': 'warning',
                'text': "Districts containing >1 stations : %i" % (districts_report.get_districts_containing_more_stations())
            })
            self.report.append({ 'style': None,
                'text': "\n"
            })

    def build_residential_address_report(self):
        address_report = ResidentialAddressReport(self.council_id)

        addresses_imported = address_report.get_addresses_imported()
        if addresses_imported > 0:
            self.report.append({ 'style': 'bold',
                'text': "ADDRESSES IMPORTED               : %i" % (addresses_imported)
            })
            self.report.append({ 'style': None,
                'text': "----------------------------------"
            })

            station_ids = address_report.get_addresses_with_station_id()
            if station_ids > 0:
                self.report.append({ 'style': 'ok_bold',
                    'text': " - with station id               : %i" % (station_ids)
                })
                self.report.append({ 'style': 'ok',
                    'text': "   - valid station id refs       : %i" % (address_report.get_addresses_with_valid_station_id_ref())
                })
                self.report.append({ 'style': 'warning',
                    'text': "   - invalid station id refs     : %i" % (address_report.get_addresses_with_invalid_station_id_ref())
                })
            else:
                self.report.append({ 'style': 'ok',
                    'text': " - with station id               : %i" % (station_ids)
                })

            self.report.append({ 'style': 'warning',
                'text': " - without station id            : %i" % (address_report.get_addresses_without_station_id())
            })
            self.report.append({ 'style': None,
                'text': "\n"
            })

    def build_report(self):
        self.build_header()
        self.build_district_report()
        self.build_station_report()
        self.build_residential_address_report()

    def output_console_report(self):
        for line in self.report:
            if line['style'] == 'ok':
                OutputFormatter.print_ok(line['text'])
            elif line['style'] == 'warning':
                OutputFormatter.print_warning(line['text'])
            elif line['style'] == 'ok_bold':
                OutputFormatter.print_ok_bold(line['text'])
            elif line['style'] == 'bold':
                OutputFormatter.print_bold(line['text'])
            elif line['style'] is None:
                print(line['text'])

    def generate_string_report(self):
        out = ''
        for line in self.report:
            out = out + line['text'] + "\n"
        return out.strip()
