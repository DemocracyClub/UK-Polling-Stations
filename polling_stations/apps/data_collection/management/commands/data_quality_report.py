from django.apps import apps
from django.core.management.base import BaseCommand
from data_collection.data_quality_report import DataQualityReportBuilder


class Command(BaseCommand):
    """
    Turn off auto system check for all apps
    We will maunally run system checks only for the
    'data_collection' and 'pollingstations' apps
    """

    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            "council_id", help="Council ID to report on in the format X01000001"
        )

    def handle(self, *args, **kwargs):
        """
        Manually run system checks for the
        'data_collection' and 'pollingstations' apps
        Management commands can ignore checks that only apply to
        the apps supporting the website part of the project
        """
        self.check(
            [
                apps.get_app_config("data_collection"),
                apps.get_app_config("pollingstations"),
            ]
        )

        report = DataQualityReportBuilder(kwargs["council_id"])
        report.build_report()
        report.output_console_report()
