from django.test import TestCase

from addressbase.models import UprnToCouncil
from councils.models import Council
from pollingstations.models import PollingStation, PollingDistrict
from data_importers.models import DataQuality
from data_importers.management.commands.teardown import Command


class TestTeardown(TestCase):
    def setUp(self):
        councils = [
            {"council_id": "AAA", "identifiers": ["X01000000"]},
            {"council_id": "BBB", "identifiers": ["X01000001"]},
        ]

        for council in councils:
            Council.objects.update_or_create(**council)

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
            {"uprn": "1", "lad": "AAA", "polling_station_id": "ps1"},
            {"uprn": "2", "lad": "AAA", "polling_station_id": "ps2"},
            {"uprn": "3", "lad": "BBB", "polling_station_id": "ps1"},
        ]

        for ps in pollingstations:
            PollingStation.objects.update_or_create(**ps)

        for pd in pollingdistricts:
            PollingDistrict.objects.update_or_create(**pd)

        for uprn in uprns:
            UprnToCouncil.objects.update_or_create(**uprn)

    def test_teardown_one_council(self):
        self.assertEqual(Council.objects.count(), 2)
        self.assertEqual(PollingStation.objects.count(), 3)
        self.assertEqual(PollingDistrict.objects.count(), 3)
        self.assertListEqual(
            list(UprnToCouncil.objects.all().values_list("lad", "polling_station_id")),
            [
                ("AAA", "ps1"),
                ("AAA", "ps2"),
                ("BBB", "ps1"),
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
        cmd.handle(council="AAA")

        self.assertEqual(Council.objects.count(), 2)
        self.assertEqual(PollingStation.objects.count(), 1)
        self.assertEqual(PollingDistrict.objects.count(), 1)
        self.assertListEqual(
            sorted(
                list(
                    UprnToCouncil.objects.all().values_list("lad", "polling_station_id")
                )
            ),
            sorted(
                [
                    ("BBB", "ps1"),
                    ("AAA", ""),
                    ("AAA", ""),
                ]
            ),
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

    def test_teardown_all_councils(self):
        self.assertEqual(Council.objects.count(), 2)
        self.assertEqual(PollingStation.objects.count(), 3)
        self.assertEqual(PollingDistrict.objects.count(), 3)
        self.assertListEqual(
            list(UprnToCouncil.objects.all().values_list("lad", "polling_station_id")),
            [
                ("AAA", "ps1"),
                ("AAA", "ps2"),
                ("BBB", "ps1"),
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
            list(UprnToCouncil.objects.all().values_list("lad", "polling_station_id")),
            [("AAA", ""), ("AAA", ""), ("BBB", "")],
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
