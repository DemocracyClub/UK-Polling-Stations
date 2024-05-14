from addressbase.models import UprnToCouncil
from councils.models import Council
from django.db import connection
from django.db.models import Q
from pollingstations.models import PollingDistrict, PollingStation
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


# data quality stats for polling stations
class StationReport:
    def __init__(self, council_id, additional_report_councils=None):
        if not additional_report_councils:
            additional_report_councils = []
        self.additional_report_councils = additional_report_councils
        self.council_id = council_id
        self.councils = self.additional_report_councils + [self.council_id]
        # fmt: off
        self.counts = {
            "0": 0,
            "1": 0,
            ">1": 0
        }
        # fmt: on
        self.generate_counts()

    def get_stations_imported(self):
        return PollingStation.objects.filter(council_id__in=self.councils).count()

    def get_stations_with_district_id(self):
        return (
            PollingStation.objects.filter(
                council_id__in=self.councils, polling_district_id__isnull=False
            )
            .exclude(polling_district_id="")
            .count()
        )

    def get_stations_without_district_id(self):
        return PollingStation.objects.filter(
            Q(polling_district_id__isnull=True) | Q(polling_district_id=""),
            council_id__in=self.councils,
        ).count()

    def get_stations_with_valid_district_id_ref(self):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM pollingstations_pollingstation
            WHERE polling_district_id IN
                (SELECT internal_council_id FROM pollingstations_pollingdistrict
                WHERE council_id IN %s)
            AND council_id IN %s
            AND polling_district_id != ''
            AND polling_district_id IS NOT NULL;
            """,
            [tuple(self.councils), tuple(self.councils)],
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
                WHERE council_id IN %s)
            AND council_id IN %s
            AND polling_district_id != ''
            AND polling_district_id IS NOT NULL;
            """,
            [tuple(self.councils), tuple(self.councils)],
        )
        results = cursor.fetchall()
        return results[0][0]

    def get_stations_with_point(self):
        return PollingStation.objects.filter(
            council_id__in=self.councils, location__isnull=False
        ).count()

    def get_stations_without_point(self):
        return PollingStation.objects.filter(
            council_id__in=self.councils, location__isnull=True
        ).count()

    def get_stations_with_address(self):
        return (
            PollingStation.objects.filter(
                council_id__in=self.councils, address__isnull=False
            )
            .exclude(address="")
            .count()
        )

    def get_stations_without_address(self):
        return PollingStation.objects.filter(
            Q(address__isnull=True) | Q(address=""), council_id__in=self.councils
        ).count()

    def generate_counts(self):
        stations = PollingStation.objects.filter(council_id__in=self.councils)
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
    def __init__(self, council_id, additional_report_councils=None):
        if not additional_report_councils:
            additional_report_councils = []
        self.additional_report_councils = additional_report_councils
        self.council_id = council_id
        self.councils = self.additional_report_councils + [self.council_id]
        # fmt: off
        self.counts = {
            "0": 0,
            "1": 0,
            ">1": 0
        }
        # fmt: on
        self.generate_counts()

    def get_districts_imported(self):
        return PollingDistrict.objects.filter(council_id__in=self.councils).count()

    def get_districts_with_station_id(self):
        return (
            PollingDistrict.objects.filter(
                council_id__in=self.councils, polling_station_id__isnull=False
            )
            .exclude(polling_station_id="")
            .count()
        )

    def get_districts_without_station_id(self):
        return PollingDistrict.objects.filter(
            Q(polling_station_id__isnull=True) | Q(polling_station_id=""),
            council_id__in=self.councils,
        ).count()

    def get_districts_with_valid_station_id_ref(self):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM pollingstations_pollingdistrict
            WHERE polling_station_id IN
                (SELECT internal_council_id FROM pollingstations_pollingstation
                WHERE council_id IN %s)
            AND council_id IN %s
            AND polling_station_id != ''
            AND polling_station_id IS NOT NULL;
            """,
            [tuple(self.councils), tuple(self.councils)],
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
                WHERE council_id IN %s)
            AND council_id IN %s
            AND polling_station_id != ''
            AND polling_station_id IS NOT NULL;
            """,
            [tuple(self.councils), tuple(self.councils)],
        )
        results = cursor.fetchall()
        return results[0][0]

    def generate_counts(self):
        districts = PollingDistrict.objects.filter(council_id__in=self.councils)
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


# data quality stats for UPRNs assigned polling station ids
class AddressReport:
    def __init__(self, council_id, additional_report_councils=None):
        if not additional_report_councils:
            additional_report_councils = []
        self.additional_report_councils = additional_report_councils
        self.council_id = council_id
        self.councils = self.additional_report_councils + [self.council_id]
        self.gss_codes = [
            council.geography.gss
            for council in Council.objects.filter(pk__in=self.councils).select_related(
                "geography"
            )
        ]

    def get_uprns_in_addressbase(self):
        return UprnToCouncil.objects.filter(lad__in=self.gss_codes).count()

    def get_addresses_with_station_id(self):
        return (
            UprnToCouncil.objects.filter(
                lad__in=self.gss_codes, polling_station_id__isnull=False
            )
            .exclude(polling_station_id="")
            .count()
        )

    def get_addresses_without_station_id(self):
        return UprnToCouncil.objects.filter(
            Q(polling_station_id__isnull=True) | Q(polling_station_id=""),
            council_id__in=self.councils,
        ).count()

    def get_addresses_with_valid_station_id_ref(self):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM addressbase_uprntocouncil
            WHERE polling_station_id IN
                (SELECT internal_council_id FROM pollingstations_pollingstation
                WHERE council_id IN %s)
            AND lad IN %s
            AND polling_station_id != ''
            AND polling_station_id IS NOT NULL;
            """,
            [tuple(self.councils), tuple(self.gss_codes)],
        )
        results = cursor.fetchall()
        return results[0][0]

    def get_addresses_with_invalid_station_id_ref(self):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM addressbase_uprntocouncil
            WHERE polling_station_id NOT IN
                (SELECT internal_council_id FROM pollingstations_pollingstation
                WHERE council_id IN %s)
            AND lad IN %s
            AND polling_station_id != ''
            AND polling_station_id IS NOT NULL;
            """,
            [tuple(self.councils), tuple(self.gss_codes)],
        )
        results = cursor.fetchall()
        return results[0][0]


# generate all the stats
class DataQualityReportBuilder:
    def __init__(
        self,
        council_id,
        expecting_districts,
        csv_rows=None,
        additional_report_councils=None,
    ):
        self.council_id = council_id
        self.csv_rows = csv_rows
        self.report = Table.grid()
        self.additional_report_councils = additional_report_councils
        # Whether the importer is expected to have imported districts;
        # controls whether relevant summaries appear in the report.
        self.expecting_districts = expecting_districts

    def build_station_report(self):
        table = Table(title="STATIONS", show_header=False, min_width=50)
        table.add_column("Caption")
        table.add_column("Number", justify="right")

        stations_report = StationReport(
            self.council_id, additional_report_councils=self.additional_report_councils
        )

        stations_imported = stations_report.get_stations_imported()
        if stations_imported > 0:
            table.add_row(
                "STATIONS IMPORTED",
                str(stations_imported),
                style="bold",
                end_section=True,
            )

            if self.expecting_districts:
                district_ids = stations_report.get_stations_with_district_id()
                if district_ids > 0:
                    table.add_row(
                        " - with district id", str(district_ids), style="bold green"
                    )
                    table.add_row(
                        "   - valid district id refs",
                        str(stations_report.get_stations_with_valid_district_id_ref()),
                        style="green",
                    )
                    table.add_row(
                        "   - invalid district id refs",
                        str(
                            stations_report.get_stations_with_invalid_district_id_ref()
                        ),
                        style="yellow",
                    )
                else:
                    table.add_row(
                        " - with district id", str(district_ids), style="green"
                    )
                table.add_row(
                    " - without district id",
                    str(stations_report.get_stations_without_district_id()),
                    style="yellow",
                )
            table.add_row(
                " - with point",
                str(stations_report.get_stations_with_point()),
                style="green",
            )
            table.add_row(
                " - without point",
                str(stations_report.get_stations_without_point()),
                style="yellow",
            )
            table.add_row(
                " - with address",
                str(stations_report.get_stations_with_address()),
                style="green",
            )
            table.add_row(
                " - without address",
                str(stations_report.get_stations_without_address()),
                style="yellow",
                end_section=True,
            )

            if self.expecting_districts:
                table.add_row("POLYGON LOOKUPS", "", style="bold")
                table.add_row(
                    "Stations in 0 districts",
                    str(stations_report.get_stations_in_zero_districts()),
                    style="yellow",
                )
                table.add_row(
                    "Stations in 1 districts",
                    str(stations_report.get_stations_in_one_districts()),
                    style="green",
                )
                table.add_row(
                    "Stations in >1 districts",
                    str(stations_report.get_stations_in_more_districts()),
                    style="yellow",
                )

        return table

    def build_district_report(self):
        table = Table(title="DISTRICTS", show_header=False, min_width=50)
        table.add_column("Caption")
        table.add_column("Number", justify="right")

        districts_report = DistrictReport(self.council_id)

        districts_imported = districts_report.get_districts_imported()
        if self.expecting_districts:
            table.add_row(
                "DISTRICTS IMPORTED",
                str(districts_imported),
                style="bold",
                end_section=True,
            )

            station_ids = districts_report.get_districts_with_station_id()
            if station_ids > 0:
                table.add_row(
                    " - with station id", str(station_ids), style="bold green"
                )
                table.add_row(
                    "   - valid station id refs",
                    str(districts_report.get_districts_with_valid_station_id_ref()),
                    style="green",
                )
                table.add_row(
                    "   - invalid station id refs",
                    str(districts_report.get_districts_with_invalid_station_id_ref()),
                    style="yellow",
                )
            else:
                table.add_row(" - with station id", str(station_ids), style="green")

            table.add_row(
                " - without station id",
                str(districts_report.get_districts_without_station_id()),
                style="yellow",
                end_section=True,
            )
            table.add_row("POLYGON LOOKUPS", "", style="bold")
            table.add_row(
                "Districts containing 0 stations",
                str(districts_report.get_districts_containing_zero_stations()),
                style="yellow",
            )
            table.add_row(
                "Districts containing 1 stations",
                str(districts_report.get_districts_containing_one_stations()),
                style="green",
            )
            table.add_row(
                "Districts containing >1 stations",
                str(districts_report.get_districts_containing_more_stations()),
                style="yellow",
            )

        return table

    def get_csv_coverage(self, station_ids):
        return round(100 * station_ids / self.csv_rows, 1)

    def get_csv_coverage_row_color(self, station_ids):
        row_color = None
        csv_coverage = self.get_csv_coverage(station_ids)

        if csv_coverage >= 95:
            row_color = "green"
        elif csv_coverage >= 75:
            row_color = "yellow"
        else:
            row_color = "red"

        return row_color

    def build_address_report(self):
        table = Table(title="ADDRESSES", show_header=False, min_width=50)
        table.add_column("Caption")
        table.add_column("Number", justify="right")

        address_report = AddressReport(
            self.council_id, additional_report_councils=self.additional_report_councils
        )
        uprns_in_council_area = address_report.get_uprns_in_addressbase()
        addresses_imported = address_report.get_addresses_with_station_id()
        station_ids = address_report.get_addresses_with_station_id()
        if addresses_imported > 0:
            valid_station_ids = address_report.get_addresses_with_valid_station_id_ref()
            invalid_station_ids = (
                address_report.get_addresses_with_invalid_station_id_ref()
            )
            invalid_station_ids_row_color = (
                "green" if invalid_station_ids == 0 else "red"
            )

            table.add_row(
                "UPRNS ASSIGNED STATION ID",
                str(station_ids),
                style="bold",
                end_section=True,
            )

            table.add_row(
                " - As % of uprns in addressbase",
                f"{round(100 * station_ids / uprns_in_council_area, 1)}%",
            )
            if self.csv_rows:
                csv_coverage = self.get_csv_coverage(station_ids)
                csv_coverage_row_color = self.get_csv_coverage_row_color(station_ids)

                table.add_row(
                    " - As % of distinct records in council csv",
                    f"{csv_coverage}%",
                    style=csv_coverage_row_color,
                )

            table.add_row(
                " - valid station id refs",
                str(valid_station_ids),
                style="green",
            )
            table.add_row(
                " - invalid station id refs",
                str(invalid_station_ids),
                style=invalid_station_ids_row_color,
            )
        else:
            table.add_row(
                "NO POLLING STATIONS ASSIGNED", "", style="yellow", end_section=True
            )
        return table

    def build_report(self):
        self.report.add_row(
            Panel(Text("DATA QUALITY REPORT", justify="center", style="bold"))
        )
        if self.expecting_districts:
            self.report.add_row(self.build_district_report())
        self.report.add_row(self.build_station_report())
        self.report.add_row(self.build_address_report())

    def generate_string_report(self):
        recorder = Console(record=True)
        recorder.print(self.report)
        return recorder.export_text()
