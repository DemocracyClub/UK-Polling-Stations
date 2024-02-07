import datetime

from addressbase.models import UprnToCouncil
from addressbase.tests.factories import UprnToCouncilFactory
from councils.tests.factories import CouncilFactory
from data_importers.event_types import DataEventType
from data_importers.tests.factories import DataEventFactory
from django.test import TestCase
from pollingstations.tests.factories import PollingStationFactory


class TestAddressFactory(TestCase):
    def test_get_council_from_others_in_postcode(self):
        council_abc = CouncilFactory(pk="ABC", identifiers=["X01000000"])
        UprnToCouncilFactory.create_batch(3, lad="X01000000", uprn__postcode="AA11AA")

        uprns = UprnToCouncil.objects.all()
        uprn = uprns[0]
        address = uprn.uprn
        uprn.delete()
        self.assertEqual(address.get_council_from_others_in_postcode(), council_abc)

    def test_get_council_from_others_in_postcode_ambiguous(self):
        CouncilFactory(pk="ABC", identifiers=["X01000000"])
        UprnToCouncilFactory.create_batch(2, lad="X01000000", uprn__postcode="AA11AA")
        UprnToCouncilFactory.create_batch(2, lad="X01000002", uprn__postcode="AA11AA")
        uprns = UprnToCouncil.objects.filter(lad="X01000000")
        uprn = uprns[0]
        address = uprn.uprn
        uprn.delete()
        self.assertIsNone(address.get_council_from_others_in_postcode())

    def test_polling_station_with_elections(self):
        council_foo = CouncilFactory(pk="FOO", identifiers=["X012345"])
        DataEventFactory(
            council=council_foo,
            event_type=DataEventType.IMPORT,
            election_dates=[datetime.date(year=2024, month=5, day=2)],
        )
        ps = PollingStationFactory(council=council_foo)
        uprn_with_station = UprnToCouncilFactory(
            lad=council_foo.identifiers[0], polling_station_id=ps.internal_council_id
        )
        uprn_without_station = UprnToCouncilFactory(lad=council_foo.identifiers[0])
        ps_with_elections = uprn_with_station.uprn.polling_station_with_elections
        self.assertEqual(
            ps_with_elections.elections, [datetime.date(year=2024, month=5, day=2)]
        )
        self.assertIsNone(uprn_without_station.uprn.polling_station_with_elections)
