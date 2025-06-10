from data_importers.models import DataEvent
from councils.models import Council
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.management.base import CommandParser
from data_importers.management.commands.teardown import Command as TeardownCommand
from data_importers.event_types import DataEventType


class Command(BaseCommand):
    help = "Delete data relevant to elections that are in the past"

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
                """
                Get the latest event of type IMPORT or TEARDOWN

                If the most recent event is a TEARDOWN we can skip this council

                If the most recent event is an IMPORT we will use the data to
                decide if we want to keep this data or delete it.

                If the latest event is a SET_STATION_VISIBILITY that doesn't
                tell us anything in this context. We just want to look at the
                IMPORT event prior to any SET_STATION_VISIBILITY events.
                """
                latest_event = (
                    DataEvent.objects.filter(council=council)
                    .filter(
                        event_type__in=[DataEventType.IMPORT, DataEventType.TEARDOWN]
                    )
                    .latest("created")
                )

                if (
                    latest_event.event_type == DataEventType.IMPORT
                    and latest_event.election_dates
                    and all(
                        date < timezone.now().date()
                        for date in latest_event.election_dates
                    )
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
            cmd.teardown_councils(councils_to_teardown)

            self.stdout.write("")

            for council in councils_to_ignore:
                self.stdout.write(
                    f"Preserving data for: {council.name} ({council.council_id})..."
                )
