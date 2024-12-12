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
        ni_councils = [
            {"council_id": "ANN", "identifiers": ["N09000001"]},
            {"council_id": "ABC", "identifiers": ["N09000002"]},
            {"council_id": "BFS", "identifiers": ["N09000003"]},
            {"council_id": "CCG", "identifiers": ["N09000004"]},
            {"council_id": "DRS", "identifiers": ["N09000005"]},
            {"council_id": "FMO", "identifiers": ["N09000006"]},
            {"council_id": "LBC", "identifiers": ["N09000007"]},
            {"council_id": "MEA", "identifiers": ["N09000008"]},
            {"council_id": "MUL", "identifiers": ["N09000009"]},
            {"council_id": "NMD", "identifiers": ["N09000010"]},
            {"council_id": "AND", "identifiers": ["N09000011"]},
        ]

        for council in councils + ni_councils:
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

        for ni_council in ni_councils:
            council_id = ni_council["council_id"]
            identifier = ni_council["identifiers"][0]
            ps_internal_council_id = f"ps-{council_id}"
            pollingstations.append(
                {
                    "council": Council.objects.get(pk=council_id),
                    "internal_council_id": ps_internal_council_id,
                }
            )
            uprns.append(
                {
                    "uprn": identifier[2:],
                    "lad": identifier,
                    "polling_station_id": ps_internal_council_id,
                }
            )

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

        self.uprn_lad_ps = [
            ("N09000001", "ps-ANN"),
            ("N09000002", "ps-ABC"),
            ("N09000003", "ps-BFS"),
            ("N09000004", "ps-CCG"),
            ("N09000005", "ps-DRS"),
            ("N09000006", "ps-FMO"),
            ("N09000007", "ps-LBC"),
            ("N09000008", "ps-MEA"),
            ("N09000009", "ps-MUL"),
            ("N09000010", "ps-NMD"),
            ("N09000011", "ps-AND"),
            ("X01000000", "ps1"),
            ("X01000000", "ps2"),
            ("X01000001", "ps1"),
        ]

    def test_teardown_one_council(self):
        self.assertEqual(Council.objects.count(), 13)
        self.assertEqual(PollingStation.objects.count(), 14)
        self.assertEqual(PollingDistrict.objects.count(), 3)
        self.assertListEqual(
            sorted(
                UprnToCouncil.objects.all().values_list("lad", "polling_station_id")
            ),
            self.uprn_lad_ps,
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

        self.assertEqual(Council.objects.count(), 13)
        self.assertEqual(PollingStation.objects.count(), 12)
        self.assertEqual(PollingDistrict.objects.count(), 1)
        self.assertListEqual(
            sorted(
                UprnToCouncil.objects.all().values_list("lad", "polling_station_id")
            ),
            [  # Only one council's stations have been remove from uprntocouncil table (id X01000000)
                ("N09000001", "ps-ANN"),
                ("N09000002", "ps-ABC"),
                ("N09000003", "ps-BFS"),
                ("N09000004", "ps-CCG"),
                ("N09000005", "ps-DRS"),
                ("N09000006", "ps-FMO"),
                ("N09000007", "ps-LBC"),
                ("N09000008", "ps-MEA"),
                ("N09000009", "ps-MUL"),
                ("N09000010", "ps-NMD"),
                ("N09000011", "ps-AND"),
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

    def test_teardown_eoni(self):
        self.assertEqual(Council.objects.count(), 13)
        self.assertEqual(PollingStation.objects.count(), 14)
        self.assertEqual(PollingDistrict.objects.count(), 3)
        self.assertListEqual(
            sorted(
                UprnToCouncil.objects.all().values_list("lad", "polling_station_id")
            ),
            self.uprn_lad_ps,
        )

        cmd = Command()
        cmd.handle(council=None, eoni=True)

        self.assertEqual(Council.objects.count(), 13)
        self.assertEqual(PollingStation.objects.count(), 3)
        self.assertEqual(PollingDistrict.objects.count(), 3)
        self.assertListEqual(
            sorted(
                UprnToCouncil.objects.all().values_list("lad", "polling_station_id")
            ),
            [  # NI stations removed from uprntocounciltable
                ("N09000001", ""),
                ("N09000002", ""),
                ("N09000003", ""),
                ("N09000004", ""),
                ("N09000005", ""),
                ("N09000006", ""),
                ("N09000007", ""),
                ("N09000008", ""),
                ("N09000009", ""),
                ("N09000010", ""),
                ("N09000011", ""),
                ("X01000000", "ps1"),
                ("X01000000", "ps2"),
                ("X01000001", "ps1"),
            ],
        )

    def test_teardown_all_councils(self):
        self.assertEqual(Council.objects.count(), 13)
        self.assertEqual(PollingStation.objects.count(), 14)
        self.assertEqual(PollingDistrict.objects.count(), 3)
        self.assertListEqual(
            sorted(
                UprnToCouncil.objects.all().values_list("lad", "polling_station_id")
            ),
            self.uprn_lad_ps,
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

        self.assertEqual(Council.objects.count(), 13)
        self.assertEqual(PollingStation.objects.count(), 0)
        self.assertEqual(PollingDistrict.objects.count(), 0)
        self.assertListEqual(
            sorted(
                UprnToCouncil.objects.all().values_list("lad", "polling_station_id")
            ),
            [  # All stations removed from uprntocounciltable
                ("N09000001", ""),
                ("N09000002", ""),
                ("N09000003", ""),
                ("N09000004", ""),
                ("N09000005", ""),
                ("N09000006", ""),
                ("N09000007", ""),
                ("N09000008", ""),
                ("N09000009", ""),
                ("N09000010", ""),
                ("N09000011", ""),
                ("X01000000", ""),
                ("X01000000", ""),
                ("X01000001", ""),
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
            DataEvent.objects.filter(event_type=DataEventType.TEARDOWN).count(), 13
        )
