from addressbase.models import Address, UprnToCouncil
from addressbase.tests.factories import UprnToCouncilFactory
from councils.tests.factories import CouncilFactory
from data_importers.management.commands.import_misc_fixes import (
    assign_addresses_by_district,
    delete_council_data,
    remove_points_from_addressbase,
    unassign_addresses_by_district,
    unassign_uprns,
    update_station_address,
    update_station_point,
)
from django.contrib.gis.geos import MultiPolygon, Point, Polygon
from django.test import TestCase
from pollingstations.models import PollingDistrict, PollingStation
from pollingstations.tests.factories import (
    PollingDistrictFactory,
    PollingStationFactory,
)


class XpressDemocracyClubImportTests(TestCase):
    def setUp(self):
        CouncilFactory.create(council_id="FOO", identifiers=["E000001"])
        self.station_123 = PollingStationFactory.create(
            council_id="FOO",
            internal_council_id="123",
            address="station address",
            postcode="AA1 1AA",
            location=Point(-4, 50, srid=4326),
        )
        self.station_456 = PollingStationFactory.create(
            council_id="FOO",
            internal_council_id="456",
        )

        self.district_AB = PollingDistrictFactory.create(
            council_id="FOO",
            internal_council_id="AB",
            area=MultiPolygon(
                Polygon(((-5, 45), (-5, 60), (-1, 60), (-1, 45), (-5, 45)))
            ),
        )

        UprnToCouncilFactory.create(
            uprn__uprn="000000000",
            lad="E000001",
            polling_station_id="123",
            uprn__location=Point(-3, 48),
        )
        UprnToCouncilFactory.create(
            uprn__uprn="000000001",
            lad="E000001",
            polling_station_id="123",
            uprn__location=Point(-6, 48),
        )

        UprnToCouncilFactory.create(
            uprn__uprn="000000002",
            lad="E000001",
            polling_station_id="456",
            uprn__location=Point(),
        )

    def test_update_station_point(self):
        self.assertEqual(self.station_123.location.coords, (-4, 50))
        update_station_point("FOO", "123", Point(-2, 55, srid=4326))
        self.station_123.refresh_from_db()
        self.assertEqual(self.station_123.location.coords, (-2, 55))

    def test_update_station_address(self):
        update_station_address("FOO", "123", address="new address")
        self.station_123.refresh_from_db()
        self.assertEqual(self.station_123.address, "new address")
        self.assertEqual(self.station_123.postcode, "")

    def test_update_station_address_and_postcode(self):
        update_station_address(
            "FOO", "123", address="another new address", postcode="AA2 2AA"
        )
        self.station_123.refresh_from_db()
        self.assertEqual(self.station_123.address, "another new address")
        self.assertEqual(self.station_123.postcode, "AA2 2AA")

    def test_update_station_postcode(self):
        update_station_address("FOO", "123", postcode="AA3 3AA")
        self.station_123.refresh_from_db()
        self.assertEqual(self.station_123.address, "station address")
        self.assertEqual(self.station_123.postcode, "AA3 3AA")

    def test_assign_addresses_by_district(self):
        self.assertEqual(
            set(
                UprnToCouncil.objects.filter(polling_station_id="123").values_list(
                    "uprn", flat=True
                )
            ),
            {"000000000", "000000001"},
        )
        assign_addresses_by_district("FOO", "AB", "456")
        self.assertEqual(
            set(
                UprnToCouncil.objects.filter(polling_station_id="123").values_list(
                    "uprn", flat=True
                )
            ),
            {"000000001"},
        )
        self.assertEqual(
            set(
                UprnToCouncil.objects.filter(polling_station_id="456").values_list(
                    "uprn", flat=True
                )
            ),
            {"000000000", "000000002"},
        )

    def test_unassign_addresses_by_district(self):
        self.assertEqual(
            len(
                UprnToCouncil.objects.filter(polling_station_id="123").values_list(
                    "uprn", flat=True
                )
            ),
            2,
        )
        unassign_addresses_by_district("FOO", "AB")
        self.assertEqual(
            len(
                UprnToCouncil.objects.filter(polling_station_id="123").values_list(
                    "uprn", flat=True
                )
            ),
            1,
        )

    def test_unassign_uprns(self):
        self.assertEqual(
            len(
                UprnToCouncil.objects.filter(polling_station_id="").values_list(
                    "uprn", flat=True
                )
            ),
            0,
        )
        unassign_uprns(["000000000", "000000001", "000000002"])
        self.assertEqual(
            len(
                UprnToCouncil.objects.filter(polling_station_id="").values_list(
                    "uprn", flat=True
                )
            ),
            3,
        )

    def test_remove_points_from_addressbase(self):
        self.assertTrue(Address.objects.filter(uprn="000000000").exists())
        self.assertTrue(UprnToCouncil.objects.filter(uprn="000000000").exists())
        remove_points_from_addressbase(["000000000"])
        self.assertFalse(Address.objects.filter(uprn="000000000").exists())
        self.assertFalse(UprnToCouncil.objects.filter(uprn="000000000").exists())

    def test_delete_council_data(self):
        self.assertTrue(PollingStation.objects.filter(council_id="FOO").exists())
        self.assertTrue(PollingDistrict.objects.filter(council_id="FOO").exists())
        self.assertTrue(
            UprnToCouncil.objects.filter(lad="E000001")
            .exclude(polling_station_id="")
            .exists()
        )
        delete_council_data("FOO")

        self.assertFalse(PollingStation.objects.filter(council_id="FOO").exists())
        self.assertFalse(PollingDistrict.objects.filter(council_id="FOO").exists())
        self.assertFalse(
            UprnToCouncil.objects.filter(lad="E000001")
            .exclude(polling_station_id="")
            .exists()
        )
