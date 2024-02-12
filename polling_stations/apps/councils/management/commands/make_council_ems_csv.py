import csv
import re
from pathlib import Path

from councils.models import Council
from django.core.management.base import BaseCommand
from django.utils import timezone

from polling_stations.settings.constants.councils import NIR_IDS

IMPORT_CLASS_TO_EMS_DICT = {
    "BaseXpressCsvImporter": "Xpress Other",
    "BaseXpressWebLookupCsvImporter": "Xpress WebLookup",
    "BaseXpressDemocracyClubCsvImporter": "Xpress DC",
    "BaseXpressDCCsvInconsistentPostcodesImporter": "Xpress DC",
    "BaseHalaroseCsvImporter": "Idox Eros (Halarose)",
    "BaseDemocracyCountsCsvImporter": "Democracy Counts",
    "BaseFcsDemocracyClubApiImporter": "FCS API",
    "BaseGitHubImporter": "Scraper API",
    "BaseStationsDistrictsImporter": "Stations & Districts geo",
}


def extract_line_with_string(file_path, search_string):
    try:
        with open(file_path, "r") as file:
            for line in file:
                if search_string in line:
                    return line
    except FileNotFoundError:
        return ""
    return ""


def extract_ems_importer_class(input_string):
    pattern = re.compile(
        r"""
        BaseXpressCsvImporter |
        BaseXpressWebLookupCsvImporter |
        BaseXpressDemocracyClubCsvImporter |
        BaseXpressDCCsvInconsistentPostcodesImporter |
        BaseHalaroseCsvImporter |
        BaseDemocracyCountsCsvImporter |
        BaseFcsDemocracyClubApiImporter |
        BaseGitHubImporter |
        BaseStationsDistrictsImporter
    """,
        re.VERBOSE,
    )
    match = re.search(pattern, input_string)
    if match:
        return match.group()

    return ""


def get_ems_from_import_script(council):
    if council.council_id in NIR_IDS:
        return "EONI"
    importer_class_line = extract_line_with_string(
        council.import_script_path, "class Command"
    )
    importer_class = extract_ems_importer_class(importer_class_line)
    if not importer_class:
        return ""
    return IMPORT_CLASS_TO_EMS_DICT[importer_class]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-f",
            "--file",
            default="council_ems.csv",
            action="store",
            required=False,
            help="File path for CSV. Default 'council_ems.csv'",
        )

    def handle(self, **options):
        filepath = Path(options["file"])
        data = []
        for council in Council.objects.with_ems_from_uploads():
            row_dict = {
                "Council ID": council.council_id,
                "Council Name": council.name,
                "EMS": council.latest_ems,
                "EMS Source": f"Upload: {council.latest_upload_id}",
            }

            if not council.latest_ems:
                row_dict["EMS"] = get_ems_from_import_script(council)
                row_dict["EMS Source"] = f"import script ({timezone.now().date()})"
            data.append(row_dict)
            if not row_dict["EMS"]:
                self.stdout.write(
                    f"No EMS found for {council.name} ({council.council_id})"
                )

        with filepath.open("w", newline="") as csv_file:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
