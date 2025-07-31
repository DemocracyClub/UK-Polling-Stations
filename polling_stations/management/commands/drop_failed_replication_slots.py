from datetime import date
from typing import Dict, Any

from django.core.management.base import BaseCommand
from django.conf import settings

from core.slack_client import SlackClient
from settings.constants.slack import BOTS_CHANNEL, BOTS_TESTING_CHANNEL
from polling_stations.db_routers import (
    get_principal_db_name,
    get_principal_db_connection,
)

DB_NAME = get_principal_db_name()


class Command(BaseCommand):
    help = "Checks for failed replication slots in RDS and drops them, then reports to Slack"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post_to_slack = False
        self.dc_environment = None
        self.cursor = get_principal_db_connection().cursor()
        self.slack_client = SlackClient(channel=self.slack_channel)
        self.failed_slots = []
        self.drop_succeeded = []
        self.drop_failed = []

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--send-slack-report",
            action="store_true",
            help="Ask import_eoni command to report to slack",
        )

    def handle(self, *args, **options):
        try:
            self.dc_environment = settings.DC_ENVIRONMENT
            self.post_to_slack = options.get("post_to_slack")
            self.check_replication_slots()

            if self.failed_slots:
                self.drop_failed_slots()
                self.report_to_slack()
                return

            if date.today().weekday() == 0:
                # Report once a week even if no failed slots found, so we know bot is working.
                self.report_to_slack()
                return

        except Exception as e:
            self.send_failure_to_slack(e)
            raise e

    @property
    def slack_channel(self):
        if self.dc_environment == "production":
            return BOTS_CHANNEL
        else:
            return BOTS_TESTING_CHANNEL

    def check_replication_slots(self):
        with get_principal_db_connection().cursor() as cursor:
            query = """
                    SELECT
                        slot_name
                    FROM pg_replication_slots
                    WHERE
                       active = 'f'
                       AND database = %s
                    ORDER BY slot_name;
                    """

            cursor.execute(query, [DB_NAME])

            for row in cursor.fetchall():
                self.failed_slots.append(row[0])

    def report_to_slack(self):
        if not self.post_to_slack:
            return
        try:
            response = self.post_thread_header()
            thread_ts = response.get("ts")
            if self.failed_slots:
                self.post_failed_details(thread_ts)
            else:
                self.post_check_running(thread_ts)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error posting to Slack: {str(e)}"))
            raise e

    def post_thread_header(self) -> Dict[str, Any]:
        return self.slack_client.send_message(
            message=":clipboard: *Replication Slot Check*"
        )

    def post_failed_details(self, thread_ts):
        if self.drop_succeeded:
            self.slack_client.send_message(
                message=f":white_check_mark: Dropped {len(self.drop_succeeded)} failed replication slots:\n{'\n'.join(self.drop_succeeded)}",
                thread_ts=thread_ts,
            )
        if self.drop_failed:
            self.slack_client.send_message(
                message=f":warning: Failed to drop {len(self.drop_failed)} failed replication slots:\n{'\n'.join(self.drop_failed)}",
                thread_ts=thread_ts,
            )

    def post_check_running(self, thread_ts):
        self.slack_client.send_message(
            "No failed slots found. Nightly checks are still running.",
            thread_ts=thread_ts,
        )

    def drop_replication_slot(self, cursor, slot_name):
        """Drop a replication slot"""
        try:
            self.stdout.write(f"Dropping slot {slot_name}...")
            cursor.execute("SELECT pg_drop_replication_slot(%s);", [slot_name])
            self.drop_succeeded.append(slot_name)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error dropping slot '{slot_name}': {str(e)}")
            )
            self.drop_failed.append(slot_name)

    def drop_failed_slots(self):
        with get_principal_db_connection().cursor() as cursor:
            for slot in self.failed_slots:
                self.drop_replication_slot(cursor, slot)

    def send_failure_to_slack(self, exception: Exception):
        if not self.post_to_slack:
            return
        try:
            response = self.slack_client.send_message(
                message=":warning: *drop_failed_replication_slots command failed*",
            )
            self.slack_client.send_message(
                message=f"Error: {str(exception)}", thread_ts=response.get("ts")
            )

        except Exception as slack_err:
            self.stderr.write(f"Error posting to Slack: {str(slack_err)}")
            raise slack_err
