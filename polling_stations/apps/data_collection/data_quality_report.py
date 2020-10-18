import re

from django.db import connection
from django.db.models import Q
from pollingstations.models import PollingStation, PollingDistrict, ResidentialAddress


class ANSI:
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"

    @classmethod
    def ok(cls, text):
        return cls.OKGREEN + text + cls.ENDC

    @classmethod
    def warning(cls, text):
        return cls.WARNING + text + cls.ENDC

    @classmethod
    def bold(cls, text):
        return cls.BOLD + text + cls.ENDC

    @classmethod
    def ok_bold(cls, text):
        return cls.OKGREEN + cls.BOLD + text + cls.ENDC

    @staticmethod
    def remove_escapes(text):
        return re.sub("\033\\[[0-9;]+m", "", text)


# data quality stats for polling stations
class StationReport:
    def __init__(self, council_id):
        self.council_id = council_id
        # fmt: off
        self.counts = {
            "0": 0,
            "1": 0,
            ">1": 0
        }
        # fmt: on
        self.generate_counts()

    def get_stations_imported(self):
        return PollingStation.objects.filter(council_id=self.council_id).count()

    def get_stations_with_district_id(self):
        return (
            PollingStation.objects.filter(
                council_id=self.council_id, polling_district_id__isnull=False
            )
            .exclude(polling_district_id="")
            .count()
        )

    def get_stations_without_district_id(self):
        return PollingStation.objects.filter(
            Q(polling_district_id__isnull=True) | Q(polling_district_id=""),
            council_id=self.council_id,
        ).count()

    def get_stations_with_valid_district_id_ref(self):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM pollingstations_pollingstation
            WHERE polling_district_id IN
                (SELECT internal_council_id FROM pollingstations_pollingdistrict
                WHERE council_id=%s)
            AND council_id=%s
            AND polling_district_id != ''
            AND polling_district_id IS NOT NULL;
            """,
            [self.council_id, self.council_id],
        )
        results = cursor.fetchall()
        return results[0][0]

    def get_stations_with_invalid_district_id_ref(self):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM pollingstations_pollingstation
            WHERE polling_district_id NOT IN
                (SELECT internal_council_id FROM pollingstations_pollingdistrict
                WHERE council_id=%s)
            AND council_id=%s
            AND polling_district_id != ''
            AND polling_district_id IS NOT NULL;
            """,
            [self.council_id, self.council_id],
        )
        results = cursor.fetchall()
        return results[0][0]

    def get_stations_with_point(self):
        return PollingStation.objects.filter(
            council_id=self.council_id, location__isnull=False
        ).count()

    def get_stations_without_point(self):
        return PollingStation.objects.filter(
            council_id=self.council_id, location__isnull=True
        ).count()

    def get_stations_with_address(self):
        return (
            PollingStation.objects.filter(
                council_id=self.council_id, address__isnull=False
            )
            .exclude(address="")
            .count()
        )

    def get_stations_without_address(self):
        return PollingStation.objects.filter(
            Q(address__isnull=True) | Q(address=""), council_id=self.council_id
        ).count()

    def generate_counts(self):
        stations = PollingStation.objects.filter(council_id=self.council_id)
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
                self.counts["0"] = self.counts["0"] + 1
            elif count == 1:
                self.counts["1"] = self.counts["1"] + 1
            else:
                self.counts[">1"] = self.counts[">1"] + 1

    def get_stations_in_zero_districts(self):
        return self.counts["0"]

    def get_stations_in_one_districts(self):
        return self.counts["1"]

    def get_stations_in_more_districts(self):
        return self.counts[">1"]


# data quality stats for polling districts
class DistrictReport:
    def __init__(self, council_id):
        self.council_id = council_id
        # fmt: off
        self.counts = {
            "0": 0,
            "1": 0,
            ">1": 0
        }
        # fmt: on
        self.generate_counts()

    def get_districts_imported(self):
        return PollingDistrict.objects.filter(council_id=self.council_id).count()

    def get_districts_with_station_id(self):
        return (
            PollingDistrict.objects.filter(
                council_id=self.council_id, polling_station_id__isnull=False
            )
            .exclude(polling_station_id="")
            .count()
        )

    def get_districts_without_station_id(self):
        return PollingDistrict.objects.filter(
            Q(polling_station_id__isnull=True) | Q(polling_station_id=""),
            council_id=self.council_id,
        ).count()

    def get_districts_with_valid_station_id_ref(self):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM pollingstations_pollingdistrict
            WHERE polling_station_id IN
                (SELECT internal_council_id FROM pollingstations_pollingstation
                WHERE council_id=%s)
            AND council_id=%s
            AND polling_station_id != ''
            AND polling_station_id IS NOT NULL;
            """,
            [self.council_id, self.council_id],
        )
        results = cursor.fetchall()
        return results[0][0]

    def get_districts_with_invalid_station_id_ref(self):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM pollingstations_pollingdistrict
            WHERE polling_station_id NOT IN
                (SELECT internal_council_id FROM pollingstations_pollingstation
                WHERE council_id=%s)
            AND council_id=%s
            AND polling_station_id != ''
            AND polling_station_id IS NOT NULL;
            """,
            [self.council_id, self.council_id],
        )
        results = cursor.fetchall()
        return results[0][0]

    def generate_counts(self):
        districts = PollingDistrict.objects.filter(council_id=self.council_id)
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
                self.counts["0"] = self.counts["0"] + 1
            elif count == 1:
                self.counts["1"] = self.counts["1"] + 1
            else:
                self.counts[">1"] = self.counts[">1"] + 1

    def get_districts_containing_zero_stations(self):
        return self.counts["0"]

    def get_districts_containing_one_stations(self):
        return self.counts["1"]

    def get_districts_containing_more_stations(self):
        return self.counts[">1"]


# data quality stats for residential addresses
class ResidentialAddressReport:
    def __init__(self, council_id):
        self.council_id = council_id

    def get_addresses_imported(self):
        return ResidentialAddress.objects.filter(council_id=self.council_id).count()

    def get_addresses_with_station_id(self):
        return (
            ResidentialAddress.objects.filter(
                council_id=self.council_id, polling_station_id__isnull=False
            )
            .exclude(polling_station_id="")
            .count()
        )

    def get_addresses_without_station_id(self):
        return ResidentialAddress.objects.filter(
            Q(polling_station_id__isnull=True) | Q(polling_station_id=""),
            council_id=self.council_id,
        ).count()

    def get_uprns_imported(self):
        return (
            ResidentialAddress.objects.filter(council_id=self.council_id)
            .exclude(uprn="")
            .count()
        )

    def get_addresses_with_valid_station_id_ref(self):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM pollingstations_residentialaddress
            WHERE polling_station_id IN
                (SELECT internal_council_id FROM pollingstations_pollingstation
                WHERE council_id=%s)
            AND council_id=%s
            AND polling_station_id != ''
            AND polling_station_id IS NOT NULL;
            """,
            [self.council_id, self.council_id],
        )
        results = cursor.fetchall()
        return results[0][0]

    def get_addresses_with_invalid_station_id_ref(self):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM pollingstations_residentialaddress
            WHERE polling_station_id NOT IN
                (SELECT internal_council_id FROM pollingstations_pollingstation
                WHERE council_id=%s)
            AND council_id=%s
            AND polling_station_id != ''
            AND polling_station_id IS NOT NULL;
            """,
            [self.council_id, self.council_id],
        )
        results = cursor.fetchall()
        return results[0][0]


# generate all the stats
class DataQualityReportBuilder:
    def __init__(self, council_id, expecting_districts):
        self.council_id = council_id
        self.report = []
        # Whether the importer is expected to have imported districts;
        # controls whether relevant summaries appear in the report.
        self.expecting_districts = expecting_districts

    def build_header(self):
        self.report.append("==================================")
        self.report.append(ANSI.bold("        DATA QUALITY REPORT"))
        self.report.append("==================================\n")

    def build_station_report(self):
        stations_report = StationReport(self.council_id)

        stations_imported = stations_report.get_stations_imported()
        if stations_imported > 0:
            self.report.append(
                ANSI.bold("STATIONS IMPORTED                : %i" % (stations_imported))
            )
            self.report.append("----------------------------------")

            if self.expecting_districts:
                district_ids = stations_report.get_stations_with_district_id()
                if district_ids > 0:
                    self.report.append(
                        ANSI.ok_bold(
                            " - with district id              : %i" % (district_ids)
                        )
                    )
                    self.report.append(
                        ANSI.ok(
                            "   - valid district id refs      : %i"
                            % (
                                stations_report.get_stations_with_valid_district_id_ref()
                            ),
                        )
                    )
                    self.report.append(
                        ANSI.warning(
                            "   - invalid district id refs    : %i"
                            % (
                                stations_report.get_stations_with_invalid_district_id_ref()
                            )
                        )
                    )
                else:
                    self.report.append(
                        ANSI.ok(
                            " - with district id              : %i" % (district_ids)
                        )
                    )

                self.report.append(
                    ANSI.warning(
                        " - without district id           : %i"
                        % (stations_report.get_stations_without_district_id())
                    )
                )
            self.report.append(
                ANSI.ok(
                    " - with point                    : %i"
                    % (stations_report.get_stations_with_point())
                )
            )
            self.report.append(
                ANSI.warning(
                    " - without point                 : %i"
                    % (stations_report.get_stations_without_point()),
                )
            )
            self.report.append(
                ANSI.ok(
                    " - with address                  : %i"
                    % (stations_report.get_stations_with_address()),
                )
            )
            self.report.append(
                ANSI.warning(
                    " - without address               : %i"
                    % (stations_report.get_stations_without_address())
                )
            )
            if self.expecting_districts:
                self.report.append("----------------------------------")
                self.report.append(ANSI.bold("POLYGON LOOKUPS"))
                self.report.append(
                    ANSI.warning(
                        "Stations in 0 districts          : %i"
                        % (stations_report.get_stations_in_zero_districts())
                    )
                )
                self.report.append(
                    ANSI.ok(
                        "Stations in 1 districts          : %i"
                        % (stations_report.get_stations_in_one_districts())
                    )
                )
                self.report.append(
                    ANSI.warning(
                        "Stations in >1 districts         : %i"
                        % (stations_report.get_stations_in_more_districts()),
                    )
                )
            self.report.append("\n")

    def build_district_report(self):
        districts_report = DistrictReport(self.council_id)

        districts_imported = districts_report.get_districts_imported()
        if self.expecting_districts:
            self.report.append(
                ANSI.bold(
                    "DISTRICTS IMPORTED               : %i" % (districts_imported)
                )
            )
            self.report.append("----------------------------------")

            station_ids = districts_report.get_districts_with_station_id()
            if station_ids > 0:
                self.report.append(
                    ANSI.ok_bold(
                        " - with station id               : %i" % (station_ids),
                    )
                )
                self.report.append(
                    ANSI.ok(
                        "   - valid station id refs       : %i"
                        % (districts_report.get_districts_with_valid_station_id_ref()),
                    )
                )
                self.report.append(
                    ANSI.warning(
                        "   - invalid station id refs     : %i"
                        % (districts_report.get_districts_with_invalid_station_id_ref())
                    )
                )
            else:
                self.report.append(
                    ANSI.ok(
                        " - with station id               : %i" % (station_ids),
                    )
                )

            self.report.append(
                ANSI.warning(
                    " - without station id            : %i"
                    % (districts_report.get_districts_without_station_id()),
                )
            )
            self.report.append("----------------------------------")
            self.report.append(ANSI.bold("POLYGON LOOKUPS"))
            self.report.append(
                ANSI.warning(
                    "Districts containing 0 stations  : %i"
                    % (districts_report.get_districts_containing_zero_stations())
                )
            )
            self.report.append(
                ANSI.ok(
                    "Districts containing 1 stations  : %i"
                    % (districts_report.get_districts_containing_one_stations())
                )
            )
            self.report.append(
                ANSI.warning(
                    "Districts containing >1 stations : %i"
                    % (districts_report.get_districts_containing_more_stations()),
                )
            )
            self.report.append("\n")

    def build_residential_address_report(self):
        address_report = ResidentialAddressReport(self.council_id)

        addresses_imported = address_report.get_addresses_imported()
        if addresses_imported > 0:
            self.report.append(
                ANSI.bold(
                    "ADDRESSES IMPORTED               : %i" % (addresses_imported)
                )
            )
            self.report.append("----------------------------------")

            station_ids = address_report.get_addresses_with_station_id()
            if station_ids > 0:
                self.report.append(
                    ANSI.ok_bold(
                        " - with station id               : %i" % (station_ids),
                    )
                )
                self.report.append(
                    ANSI.ok(
                        "   - valid station id refs       : %i"
                        % (address_report.get_addresses_with_valid_station_id_ref()),
                    )
                )
                self.report.append(
                    ANSI.warning(
                        "   - invalid station id refs     : %i"
                        % (address_report.get_addresses_with_invalid_station_id_ref()),
                    )
                )
            else:
                self.report.append(
                    ANSI.ok(
                        " - with station id               : %i" % (station_ids),
                    )
                )

            self.report.append(
                ANSI.warning(
                    " - without station id            : %i"
                    % (address_report.get_addresses_without_station_id()),
                )
            )
            self.report.append("----------------------------------")
            self.report.append(
                ANSI.warning(
                    " - with UPRN                     : %i"
                    % (address_report.get_uprns_imported()),
                )
            )
            self.report.append("\n")

    def build_report(self):
        self.build_header()
        self.build_district_report()
        self.build_station_report()
        self.build_residential_address_report()

    def output_console_report(self):
        print("\n".join(self.report))

    def generate_string_report(self):
        return ANSI.remove_escapes("\n".join(self.report))
