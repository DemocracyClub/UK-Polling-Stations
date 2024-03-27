import csv
import sys
from typing import Optional

from councils.models import Council
from django.db import transaction
from pollingstations.models import AccessibilityInformation, PollingStation


class AccessibilityInformationHandler:
    def __init__(self, council):
        self.station_id_field_index = None
        self.reader = None
        self._header = None
        self.council: Council = council
        self.bool_fields = (
            "is_temporary",
            "nearby_parking",
            "disabled_parking",
            "level_access",
            "temporary_ramp",
            "hearing_loop",
            "public_toilets",
        )
        self.text_fields = (
            "getting_to_the_station",
            "at_the_station",
        )
        self.welsh_text_fields = (
            "getting_to_the_station_welsh",
            "at_the_station_welsh",
        )
        self.polling_station_fields = (
            "internal_council_id",
            "polling_station_address",
            "polling_station_postcode",
            "polling_station_uprn",
            "polling_station_identifier",
        )
        self.all_fields = (
            self.polling_station_fields
            + self.bool_fields
            + self.text_fields
            + self.welsh_text_fields
        )
        self.errors = []
        self.infos = []

    @property
    def header(self) -> list[str]:
        return self._header

    @header.setter
    def header(self, header: list[str]):
        self._header = header

    @transaction.atomic
    def handle(self, accessibility_info: list[str]):
        sys.stdout.write("Checking accessibility information csv")
        data: csv.DictReader = self.parse_data(accessibility_info)

        if self.errors:
            sys.stdout.write("\n".join(self.errors))
            return

        sys.stdout.write("Clearing existing accessibility information")
        self.delete_existing_info()

        sys.stdout.write("Importing new accessibility information")
        self.import_accessibility_info(data)

        sys.stdout.write("\n".join(self.infos))
        sys.stdout.write("\n".join(self.errors))

    def delete_existing_info(self):
        AccessibilityInformation.objects.filter(
            polling_station__council=self.council
        ).delete()

    def import_accessibility_info(self, data: csv.DictReader):
        seen = set()
        for row in data:
            if row["internal_council_id"] in seen:
                self.infos.append(
                    f"Already processed accessibility information for station id: '{row['internal_council_id']}'"
                )
                continue
            self.handle_row(row)
            seen.add(row["internal_council_id"])

    def handle_row(self, row: dict):
        def to_bool(val: str) -> Optional[bool]:
            if val.lower() in ("yes", "y"):
                return True
            if val.lower() in ("no", "n"):
                return False
            return None

        accessibility_information = {
            k: to_bool(row[k]) for k in self.bool_fields if k in row
        }
        accessibility_information.update(
            {k: row[k] for k in self.text_fields if k in row}
        )

        try:
            accessibility_information["polling_station"] = PollingStation.objects.get(
                internal_council_id=row["internal_council_id"], council=self.council
            )
        except PollingStation.DoesNotExist:
            self.errors.append(
                f"No polling station found with internal_council_id '{row['internal_council_id']}'"
            )
            return
        AccessibilityInformation.objects.create(**accessibility_information)

    def parse_data(self, accessibility_info: list[str]):
        reader = csv.reader(accessibility_info)

        try:
            self.header = next(reader)
            self.check_header()
            self.check_rows(reader)
            return csv.DictReader(accessibility_info[1:], fieldnames=self.header)
        except csv.Error as e:
            self.errors.append(
                f"Failed to parse body -> line {self.reader.line_num}: {e}"
            )

    def check_rows(self, reader):
        row_count = self.check_row_lengths(reader)
        self.check_all_rows_have_ids(reader)
        self.check_row_count_vs_station_count(row_count)

    def check_header(self):
        for field in self.all_fields:
            if field not in self.header:
                self.errors.append(f"Field: '{field}' missing from header")

        for field in self.header:
            if field not in self.all_fields:
                self.infos.append(
                    f"Unexpected field: '{field}' present in header. Ignoring."
                )

    def check_row_lengths(self, reader):
        expected_row_length = len(self.header)
        total_rows = 0
        for record in reader:
            length = len(record)
            total_rows += 1
            if length < expected_row_length:
                self.errors.append(
                    f"Wrong number of columns: Expected {expected_row_length} columns on row {total_rows} found {length}"
                )
        return total_rows

    def check_row_count_vs_station_count(self, row_count):
        station_count = self.council.pollingstation_set.count()
        if row_count != station_count:
            self.infos.append(
                f"File only has {row_count} rows, but there are {station_count} stations."
            )

    def check_all_rows_have_ids(self, reader):
        try:
            station_id_field_index = self.header.index("internal_council_id")
            if all(row[station_id_field_index] for row in reader):
                return
            self.errors.append("Some rows missing station id")
        except ValueError:
            self.errors.append("Field: 'internal_council_id' missing from header")
