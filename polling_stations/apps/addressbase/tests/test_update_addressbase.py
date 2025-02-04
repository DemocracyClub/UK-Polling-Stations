from io import StringIO
from pathlib import Path
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase, TransactionTestCase
from uk_geo_utils.base_importer import BaseImporter

from addressbase.models import Address, UprnToCouncil
from addressbase.management.commands.update_addressbase import (
    Command as UpdateAddressbaseCommand,
)
from councils.tests.factories import CouncilFactory
from pollingstations.models import PollingStation
from pollingstations.tests.factories import PollingStationFactory
from polling_stations.db_routers import get_principal_db_connection


def get_primary_key_name(table):
    with get_principal_db_connection().cursor() as cursor:
        cursor.execute(f"""
            SELECT conname
            FROM pg_constraint
            WHERE conrelid = '{table}'::regclass
            AND contype = 'p';
        """)
        names = cursor.fetchall()

        if len(names) > 1:
            raise Exception("More than one primary key name found")
        return names[0][0]


def get_foreign_key_names(table):
    with get_principal_db_connection().cursor() as cursor:
        cursor.execute(f"""
            SELECT conname
            FROM pg_constraint
            WHERE conrelid = '{table}'::regclass
            AND contype = 'f';
        """)
        return [t[0] for t in cursor.fetchall()]


class HelpersTest(TestCase):
    def setUp(self):
        with get_principal_db_connection().cursor() as cursor:
            # Create table with named primary key
            cursor.execute("""
                CREATE TABLE foo (
                    id SERIAL,
                    name VARCHAR(255),
                    CONSTRAINT foo_primary_key PRIMARY KEY (id)
                );
            """)
        with get_principal_db_connection().cursor() as cursor:
            # Create table with named foreign key
            cursor.execute("""
                CREATE TABLE bar (
                    bar_pk SERIAL PRIMARY KEY,
                    foo_id INT,
                    CONSTRAINT fk_foo_id FOREIGN KEY (foo_id) REFERENCES foo (id)
                );
            """)

    def tearDown(self):
        with get_principal_db_connection().cursor() as cursor:
            cursor.execute("""
            DROP TABLE IF EXISTS foo CASCADE;
            DROP TABLE IF EXISTS bar CASCADE;
            """)

    def test_get_primary_key_name(self):
        # __import__('ipdb').set_trace()
        self.assertEqual(get_primary_key_name("foo"), "foo_primary_key")

    def test_get_foreign_key_names(self):
        self.assertEqual(
            get_foreign_key_names("bar"),
            [
                "fk_foo_id",
            ],
        )


class UpdateAddressbaseTest(TransactionTestCase):
    def setUp(self):
        # Create some initial addresses
        # UprnToCouncilFactory.create_batch(2, lad="E07000070", uprn__postcode="AA11AA")
        self.initial_addresses = [
            Address.objects.create(
                uprn="123456789",
                address="10 Test Street",
                postcode="TE5 1ST",
                location="POINT(0 0)",
                addressbase_postal="D",
            ),
            Address.objects.create(
                uprn="9876543210",
                address="20 Test Avenue",
                postcode="TE5 2ND",
                location="POINT(1 1)",
                addressbase_postal="D",
            ),
        ]
        self.council = CouncilFactory(council_id="FOO")
        PollingStationFactory(council=self.council, internal_council_id="ps11")
        self.initial_uprns = [
            UprnToCouncil.objects.create(
                uprn=Address.objects.get(uprn="123456789"),
                lad="E07000223",
                polling_station_id="ps1",
            ),
            UprnToCouncil.objects.create(
                uprn=Address.objects.get(uprn="9876543210"), lad="E07000070"
            ),
        ]

        self.uprntocouncil_initial_values = {
            "primary_key": get_primary_key_name("addressbase_uprntocouncil"),
            "foreign_keys": get_foreign_key_names("addressbase_uprntocouncil"),
        }
        self.address_initial_values = {
            "primary_key": get_primary_key_name("addressbase_address"),
            "foreign_keys": get_foreign_key_names("addressbase_address"),
        }
        self.fixtures_dir = Path(__file__).parent / "fixtures"

    def test_success(self):
        # paths
        addressbase_path = str(
            self.fixtures_dir / "addresses_sample/addressbase_cleaned.csv"
        )
        uprntocouncil_path = str(
            self.fixtures_dir / "addresses_sample/uprntocouncil.csv"
        )

        # Initial data check
        self.assertEqual(Address.objects.count(), 2)
        self.assertEqual(UprnToCouncil.objects.count(), 2)

        # import data
        opts = {
            "addressbase_path": addressbase_path,
            "uprntocouncil_path": uprntocouncil_path,
            "stdout": StringIO(),
        }
        call_command("update_addressbase", **opts)

        self.assertEqual(Address.objects.count(), 4)
        self.assertEqual(UprnToCouncil.objects.count(), 4)
        self.assertEqual(
            get_primary_key_name("addressbase_address"),
            self.address_initial_values["primary_key"],
            msg="address primary key does not match",
        )
        self.assertEqual(
            get_foreign_key_names("addressbase_address"),
            self.address_initial_values["foreign_keys"],
            msg="address foreign key does not match",
        )
        self.assertEqual(
            get_foreign_key_names("addressbase_uprntocouncil"),
            self.uprntocouncil_initial_values["foreign_keys"],
            msg="uprntocouncil foreign key does not match",
        )
        self.assertEqual(
            get_primary_key_name("addressbase_uprntocouncil"),
            self.uprntocouncil_initial_values["primary_key"],
            msg="uprntocouncil primary key does not match",
        )
        self.assertEqual(self.council.dataevent_set.latest().event_type, "TEARDOWN")
        self.assertEqual(PollingStation.objects.count(), 0)

    def test_transaction_db_error(self):
        # paths
        addressbase_path = str(
            self.fixtures_dir / "addresses_sample/addressbase_cleaned.csv"
        )
        uprntocouncil_path = str(
            self.fixtures_dir / "addresses_sample/uprntocouncil.csv"
        )

        # Initial data check
        self.assertEqual(Address.objects.count(), 2)
        self.assertEqual(UprnToCouncil.objects.count(), 2)

        # setup command
        cmd = UpdateAddressbaseCommand()

        # supress output
        cmd.stdout = StringIO()

        # import data
        opts = {
            "addressbase_path": addressbase_path,
            "uprntocouncil_path": uprntocouncil_path,
        }
        with patch.object(BaseImporter, "rename_temp_table") as mock_rename_temp_table:
            mock_rename_temp_table.side_effect = Exception(
                "Oh no... Something went wrong renaming the temp tables"
            )

            # Run import and expect it to fail
            with self.assertRaises(Exception) as context:
                cmd.handle(**opts)
                self.assertEqual(
                    str(context.exception),
                    "Oh no... Something went wrong renaming the temp tables",
                )

        self.assertEqual(Address.objects.count(), 2)
        self.assertEqual(UprnToCouncil.objects.count(), 2)
        self.assertEqual(
            get_primary_key_name("addressbase_address"),
            self.address_initial_values["primary_key"],
            msg="address primary key does not match",
        )
        self.assertEqual(
            get_foreign_key_names("addressbase_address"),
            self.address_initial_values["foreign_keys"],
            msg="address foreign key does not match",
        )
        self.assertEqual(
            get_foreign_key_names("addressbase_uprntocouncil"),
            self.uprntocouncil_initial_values["foreign_keys"],
            msg="uprntocouncil foreign key does not match",
        )
        self.assertEqual(
            get_primary_key_name("addressbase_uprntocouncil"),
            self.uprntocouncil_initial_values["primary_key"],
            msg="uprntocouncil primary key does not match",
        )
        self.assertEqual(PollingStation.objects.count(), 1)
        self.assertEqual(self.council.dataevent_set.count(), 0)
