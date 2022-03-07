import os
import sys
import tempfile
from pathlib import Path

from django.conf import settings
from django.contrib.gis.geos import Point
from django.test import TestCase, override_settings

from addressbase.models import Address, UprnToCouncil
from councils.models import Council
from councils.tests.factories import CouncilFactory
from data_importers.base_importers import BaseImporter, BaseStationsImporter
from data_importers.data_types import StationSet
from data_importers.ems_importers import BaseXpressDemocracyClubCsvImporter
from data_importers.mixins import AdvanceVotingMixin
from pollingstations.models import PollingStation, AdvanceVotingStation
from pollingstations.tests.factories import AdvanceVotingStationFactory


class AdvanceVotingTests(TestCase):
    def setUp(self):
        self.council: Council = CouncilFactory(pk="AAA", identifiers=["X01000000"])
        self.council.save()

        uprns = ["1", "2", "3", "4", "5"]
        addressbase = [
            {
                "address": "1 Abbots Way, Lancing, West Sussex",
                "postcode": "BN15 9DH",
                "uprn": "1",
            },
            {
                "address": "2 Abbots Way, Lancing, West Sussex",
                "postcode": "BN15 9DH",
                "uprn": "2",
            },
            {
                "address": "2 Freshbrook Mews, Freshbrook Road, Lancing, West Sussex",
                "postcode": "BN15 8DA",
                "uprn": "3",
            },
            {
                "address": "2 Freshbrook Mews, Freshbrook Road, Lancing, West Sussex",
                "postcode": "BN15 8DA",
                "uprn": "4",
            },
            {
                "address": "1 Freshbrook Mews, Freshbrook Road, Lancing, West Sussex",
                "postcode": "BN15 8DA",
                "uprn": "5",
            },
        ]

        for address in addressbase:
            Address.objects.update_or_create(**address)

        for uprn in uprns:
            UprnToCouncil.objects.update_or_create(pk=uprn, lad="X01000000")

    def test_post_import_without_super(self):
        class BadAdvanceVotingImporter(BaseImporter, AdvanceVotingMixin):
            def post_import(self):
                pass

            def import_data(self):
                pass

        class GoodAdvanceVotingImporter(BaseImporter, AdvanceVotingMixin):
            def post_import(self):
                super().post_import()
                pass

            def import_data(self):
                pass

        with self.assertRaises(TypeError) as e:
            BadAdvanceVotingImporter()

        self.assertEqual(
            str(e.exception),
            "MUST Call super() in post_import when using AdvanceVotingMixin",
        )

        # This should work
        self.assertTrue(GoodAdvanceVotingImporter())

    def test_advance_polling_stations_added(self):
        class AdvanceVotingImporter(
            BaseXpressDemocracyClubCsvImporter, AdvanceVotingMixin
        ):
            council_id = "AAA"
            addresses_name = "test_democlub.csv"
            stations_name = "test_democlub.csv"
            base_folder_path = os.path.join(
                os.path.dirname(__file__), "fixtures/xpress_importer"
            )

            def add_advance_voting_stations(self):
                for i, station in enumerate(
                    PollingStation.objects.filter(council_id=self.council_id)
                ):
                    avs = AdvanceVotingStationFactory(pk=i)
                    avs.save()
                    UprnToCouncil.objects.filter(
                        polling_station_id=station.internal_council_id
                    ).update(advance_voting_station=avs)

        AdvanceVotingImporter().handle(self.council.pk, verbosity=3)
        self.assertTrue(AdvanceVotingStation.objects.all().exists())
        assigned_uprns = (
            UprnToCouncil.objects.filter(advance_voting_station_id=1)
            .order_by("uprn")
            .count()
        )

        self.assertEqual(assigned_uprns, 2)
