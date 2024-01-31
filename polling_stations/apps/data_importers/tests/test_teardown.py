from addressbase.models import Address, UprnToCouncil
from councils.models import Council
from councils.tests.factories import CouncilFactory
from data_importers.event_types import DataEventType
from data_importers.management.commands.teardown import Command
from data_importers.models import DataEvent, DataQuality
from django.test import TestCase
from pollingstations.models import PollingDistrict, PollingStation


class TestTeardown(TestCase):
    def setUp(self):
        councils = [
            {"council_id": "AAA", "identifiers": ["X01000000"]},
            {"council_id": "BBB", "identifiers": ["X01000001"]},
        ]

        for council in councils:
            CouncilFactory(**council)

        pollingstations = [
            {
                "council": Council.objects.get(pk="AAA"),
                "internal_council_id": "ps1",
            },
            {
                "council": Council.objects.get(pk="AAA"),
                "internal_council_id": "ps2",
            },
            {
                "council": Council.objects.get(pk="BBB"),
                "internal_council_id": "ps1",
            },
        ]
        pollingdistricts = [
            {
                "council": Council.objects.get(pk="AAA"),
                "internal_council_id": "pd1",
            },
            {
                "council": Council.objects.get(pk="AAA"),
                "internal_council_id": "pd2",
            },
            {
                "council": Council.objects.get(pk="BBB"),
                "internal_council_id": "pd1",
            },
        ]
        uprns = [
            {"uprn": "1", "lad": "X01000000", "polling_station_id": "ps1"},
            {"uprn": "2", "lad": "X01000000", "polling_station_id": "ps2"},
            {"uprn": "3", "lad": "X01000001", "polling_station_id": "ps1"},
        ]

        for ps in pollingstations:
            PollingStation.objects.update_or_create(**ps)

        for pd in pollingdistricts:
            PollingDistrict.objects.update_or_create(**pd)

        for uprn in uprns:
            Address.objects.update_or_create(pk=uprn["uprn"])
            UprnToCouncil.objects.update_or_create(
                pk=uprn["uprn"],
                lad=uprn["lad"],
                polling_station_id=uprn["polling_station_id"],
            )

    def test_teardown_one_council(self):
        self.assertEqual(Council.objects.count(), 2)
        self.assertEqual(PollingStation.objects.count(), 3)
        self.assertEqual(PollingDistrict.objects.count(), 3)
        self.assertListEqual(
            sorted(
                UprnToCouncil.objects.all().values_list("lad", "polling_station_id")
            ),
            [
                ("X01000000", "ps1"),
                ("X01000000", "ps2"),
                ("X01000001", "ps1"),
            ],
        )

        self.assertEqual(
            DataQuality.objects.get(council_id="AAA"),
            DataQuality(
                **{
                    "council_id": "AAA",
                    "report": "foo",
                    "num_addresses": 2,
                    "num_districts": 2,
                    "num_stations": 2,
                }
            ),
        )
        cmd = Command()
        cmd.handle(council=["AAA"])

        self.assertEqual(Council.objects.count(), 2)
        self.assertEqual(PollingStation.objects.count(), 1)
        self.assertEqual(PollingDistrict.objects.count(), 1)
        self.assertListEqual(
            sorted(
                UprnToCouncil.objects.all().values_list("lad", "polling_station_id")
            ),
            [
                ("X01000000", ""),
                ("X01000000", ""),
                ("X01000001", "ps1"),
            ],
        )
        self.assertEqual(
            DataQuality.objects.get(council_id="AAA"),
            DataQuality(
                **{
                    "council_id": "AAA",
                    "report": "",
                    "num_addresses": 0,
                    "num_districts": 0,
                    "num_stations": 0,
                }
            ),
        )
        self.assertEqual(
            DataEvent.objects.filter(event_type=DataEventType.TEARDOWN).count(), 1
        )

    def test_teardown_all_councils(self):
        self.assertEqual(Council.objects.count(), 2)
        self.assertEqual(PollingStation.objects.count(), 3)
        self.assertEqual(PollingDistrict.objects.count(), 3)
        self.assertListEqual(
            sorted(
                UprnToCouncil.objects.all().values_list("lad", "polling_station_id")
            ),
            [
                ("X01000000", "ps1"),
                ("X01000000", "ps2"),
                ("X01000001", "ps1"),
            ],
        )

        self.assertEqual(
            DataQuality.objects.get(council_id="AAA"),
            DataQuality(
                **{
                    "council_id": "AAA",
                    "report": "foo",
                    "num_addresses": 2,
                    "num_districts": 2,
                    "num_stations": 2,
                }
            ),
        )
        self.assertEqual(
            DataQuality.objects.get(council_id="AAA"),
            DataQuality(
                **{
                    "council_id": "AAA",
                    "report": "bar",
                    "num_addresses": 2,
                    "num_districts": 2,
                    "num_stations": 2,
                }
            ),
        )
        cmd = Command()
        cmd.handle(council=None, all=True)

        self.assertEqual(Council.objects.count(), 2)
        self.assertEqual(PollingStation.objects.count(), 0)
        self.assertEqual(PollingDistrict.objects.count(), 0)
        self.assertListEqual(
            sorted(
                UprnToCouncil.objects.all().values_list("lad", "polling_station_id")
            ),
            [("X01000000", ""), ("X01000000", ""), ("X01000001", "")],
        )
        self.assertEqual(
            DataQuality.objects.get(council_id="AAA"),
            DataQuality(
                **{
                    "council_id": "AAA",
                    "report": "",
                    "num_addresses": 0,
                    "num_districts": 0,
                    "num_stations": 0,
                }
            ),
        )
        self.assertEqual(
            DataQuality.objects.get(council_id="BBB"),
            DataQuality(
                **{
                    "council_id": "BBB",
                    "report": "",
                    "num_addresses": 0,
                    "num_districts": 0,
                    "num_stations": 0,
                }
            ),
        )

        self.assertEqual(
            DataEvent.objects.filter(event_type=DataEventType.TEARDOWN).count(), 2
        )
