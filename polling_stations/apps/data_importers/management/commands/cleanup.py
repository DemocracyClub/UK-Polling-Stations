from data_importers.models import DataEvent
from councils.models import Council
from django.core.management.base import BaseCommand
from django.utils import timezone
from data_importers.management.commands.teardown import Command as TeardownCommand
from django.core.management.base import CommandParser


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
        )

    def handle(self, *args, **kwargs):
        councils_to_teardown = []
        councils_to_ignore = []

        for council in Council.objects.all():
            try:
                latest_event = (
                    DataEvent.objects.filter(council=council)
                    .filter(event_type="IMPORT")
                    .latest("created")
                )

                if latest_event.election_dates and all(
                    date < timezone.now().date() for date in latest_event.election_dates
                ):
                    councils_to_teardown.append(council)
                else:
                    councils_to_ignore.append(council)

            except DataEvent.DoesNotExist:
                pass

        if kwargs.get("dry_run", False):
            for council in councils_to_teardown:
                self.stdout.write(
                    f"Would delete data for: {council.name} ({council.council_id})"
                )

            self.stdout.write("")

            for council in councils_to_ignore:
                self.stdout.write(
                    f"Would preserve data for: {council.name} ({council.council_id})"
                )
        else:
            cmd = TeardownCommand()
            for council in councils_to_teardown:
                cmd.teardown_council(council.council_id)

            self.stdout.write("")

            for council in councils_to_ignore:
                self.stdout.write(
                    f"Preserving data for: {council.name} ({council.council_id})..."
                )
