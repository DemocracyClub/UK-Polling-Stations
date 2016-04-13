from django.core.management.base import BaseCommand
from data_collection.data_quality_report import DataQualityReport

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'council_id',
            help='Council ID to report on in the format X01000001'
        )

    def handle(self, *args, **kwargs):
        report = DataQualityReport(kwargs['council_id'])
        report.build_report()
        report.output_console_report()
