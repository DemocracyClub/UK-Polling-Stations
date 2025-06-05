from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch, MagicMock
from io import StringIO
from datetime import date, timedelta
from councils.models import Council
from data_importers.models import DataEvent
from django.utils import timezone


class TestCleanup(TestCase):
    def setUp(self):
        self.councilA = Council.objects.create(council_id="AAA", name="Council A")
        self.councilB = Council.objects.create(council_id="BBB", name="Council B")
        self.councilC = Council.objects.create(council_id="CCC", name="Council C")
        self.councilD = Council.objects.create(council_id="DDD", name="Council D")

        # Past election date for council A
        DataEvent.objects.create(
            council=self.councilA,
            event_type="IMPORT",
            created=timezone.now(),
            election_dates=[date.today() - timedelta(days=10)],
        )

        # Mix of Past and Future election date for council B
        # >0 in future should be preserved
        DataEvent.objects.create(
            council=self.councilB,
            event_type="IMPORT",
            created=timezone.now(),
            election_dates=[
                date.today() - timedelta(days=10),
                date.today() + timedelta(days=10),
            ],
        )

        # Empty election dates for council C
        # should also be preserved
        DataEvent.objects.create(
            council=self.councilC,
            event_type="IMPORT",
            created=timezone.now(),
            election_dates=[],
        )

        # No DataEvent for council D

    def test_dry_run_output(self):
        out = StringIO()
        call_command("teardown_expired_data", "--dry-run", stdout=out)
        output = out.getvalue()
        self.assertIn("Would delete data for: Council A (AAA)", output)
        self.assertIn("Would preserve data for: Council B (BBB)", output)
        self.assertIn("Would preserve data for: Council C (CCC)", output)
        self.assertNotIn("Council D", output)

    @patch("data_importers.management.commands.teardown_expired_data.TeardownCommand")
    def test_teardown_called_for_past_election(self, mock_teardown_cmd):
        mock_cmd_instance = MagicMock()
        mock_teardown_cmd.return_value = mock_cmd_instance

        out = StringIO()
        call_command("teardown_expired_data", stdout=out)

        # Should call teardown_council for councilA only
        mock_cmd_instance.teardown_councils.assert_called_once_with([self.councilA])
        output = out.getvalue()
        self.assertIn("Preserving data for: Council B (BBB)...", output)
        self.assertIn("Preserving data for: Council C (CCC)", output)
        self.assertNotIn("Council D", output)
