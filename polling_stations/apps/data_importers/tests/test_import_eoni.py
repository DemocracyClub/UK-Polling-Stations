import shutil
import tempfile
from pathlib import Path

from addressbase.models import Address, UprnToCouncil
from councils.tests.factories import CouncilFactory
from data_importers.management.commands import import_eoni
from django.test import TestCase
from pollingstations.models import PollingStation

from polling_stations.settings.constants.councils import NIR_IDS

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "eoni_importer"

# A box around the coordinates in the fixture, so every imported address
# falls inside this council.
# This is just a  simplified square around an arbitary Belfast suburb:
#   https://wktmap.com/?5bcf07e5
BELFAST_GEOGRAPHY = (
    "MULTIPOLYGON ((("
    "-5.85 54.58, -5.85 54.60, -5.80 54.60, -5.80 54.58, -5.85 54.58"
    ")))"
)
BELFAST_GSS = "N09000003"


class ImportEoniTests(TestCase):
    opts = {
        "nochecks": True,
        "verbosity": 0,
        "include_past_elections": True,
        "reprojected": True,
    }

    def set_up(self, **extra_opts):
        # The command caches UPRN -> Council lookups and accumulates counts on
        # the class, so reset them tests independent of each other.
        import_eoni.UPRN_TO_COUNCIL_CACHE.clear()
        import_eoni.Command.address_counts = {council_id: 0 for council_id in NIR_IDS}
        import_eoni.Command.deduced_addresses = {}
        import_eoni.Command.removed_addresses = 0

        # Every NI council has to exist: the command iterates over NIR_IDS when
        # clearing old data, assigning UPRNs and recording import events.
        # The actual gss codes don't matter, and we only need a 'geography'
        # for Belfast.
        for i, council_id in enumerate(NIR_IDS):
            kwargs = {"pk": council_id, "identifiers": [f"N090000{i:02d}"]}
            if council_id == "BFS":
                kwargs["identifiers"] = [BELFAST_GSS]
                kwargs["geography__geography"] = BELFAST_GEOGRAPHY
            CouncilFactory(**kwargs)

        # The command writes its intermediate CSVs alongside the export, so
        # work in a temp file rather than the fixtures directory.
        self.tempdir = Path(tempfile.mkdtemp())

        # This will run at the end of the test, or if setUp fails.
        # This means clean up happens even if there's an error in setUp
        # unlike tearDown.
        self.addCleanup(
            shutil.rmtree,
            self.tempdir,
            # These kwargs are added to silence editor linter warnings.
            # They're just the defaults.
            ignore_errors=False,
            onerror=None,
            onexc=None,
            dir_fd=None,
        )

        # Copy CSV to tempdir.
        eoni_csv = self.tempdir / "eoni_export.csv"
        eoni_csv.write_bytes((FIXTURE_PATH / "eoni_export.csv").read_bytes())

        cmd = import_eoni.Command()
        cmd.handle(eoni_csv=eoni_csv, **{**self.opts, **extra_opts})

    def test_addresses(self):
        self.set_up()

        imported = Address.objects.order_by("uprn").values_list("address", flat=True)

        self.assertEqual(3, len(imported))
        expected = {
            "1 TEST STREET, BELFAST",
            "2 TEST STREET, BELFAST",
            "3 OTHER ROAD, BELFAST",
        }
        self.assertEqual(set(imported), expected)

    def test_station_ids(self):
        self.set_up()

        imported_uprns_and_ids = (
            UprnToCouncil.objects.filter(lad=BELFAST_GSS)
            .exclude(polling_station_id="")
            .order_by("uprn")
            .values_list("uprn", "polling_station_id")
        )

        expected = {
            ("100000000001", "111"),
            ("100000000002", "111"),
            ("100000000003", "222"),
        }
        self.assertEqual(set(imported_uprns_and_ids), expected)

    def test_stations(self):
        self.set_up()

        stations = (
            PollingStation.objects.filter(council_id="BFS")
            .order_by("internal_council_id")
            .values_list("internal_council_id", "address")
        )

        self.assertEqual(2, len(stations))
        expected = {
            ("111", "PUBLIC BUILDING, THE SQUARE, BELFAST, BT99 9BB"),
            ("222", "COMMUNITY CENTRE, OTHER ROAD, BELFAST, BT99 9CC"),
        }
        self.assertEqual(set(stations), expected)

    def test_station_location(self):
        self.set_up()

        station = PollingStation.objects.get(internal_council_id="111")

        self.assertEqual("BT99 9BB", station.postcode)
        self.assertAlmostEqual(-5.8310, station.location.x, places=4)
        self.assertAlmostEqual(54.5910, station.location.y, places=4)

    def test_addresses_assigned_to_council_containing_them(self):
        self.set_up()

        self.assertEqual(3, import_eoni.Command.address_counts["BFS"])
        self.assertEqual(0, import_eoni.Command.address_counts["ANN"])
        self.assertFalse(UprnToCouncil.objects.filter(lad="EONI").exists())

    def test_stations_only_leaves_addresses_alone(self):
        # With --stations-only no address data is written, so each station's
        # sample UPRN has to already be present to resolve it to a council.
        for uprn in ("100000000001", "100000000003"):
            Address.objects.create(
                uprn=uprn,
                address="PRE-EXISTING ADDRESS, BELFAST",
                postcode="BT99 9AA",
                location="SRID=4326;POINT(-5.83 54.59)",
                addressbase_postal="D",
            )
            UprnToCouncil.objects.create(uprn_id=uprn, lad=BELFAST_GSS)

        self.set_up(stations_only=True)

        self.assertEqual(2, PollingStation.objects.count())
        # The addresses that were already there are untouched
        self.assertEqual(2, Address.objects.count())
        self.assertEqual(
            ["PRE-EXISTING ADDRESS, BELFAST", "PRE-EXISTING ADDRESS, BELFAST"],
            list(Address.objects.order_by("uprn").values_list("address", flat=True)),
        )

    def test_cleanup_removes_intermediate_csvs(self):
        self.set_up(cleanup=True)

        for name in (
            "eoni_address.csv",
            "eoni_uprn_to_council.csv",
            "eoni_stations.csv",
        ):
            self.assertFalse((self.tempdir / name).exists())
