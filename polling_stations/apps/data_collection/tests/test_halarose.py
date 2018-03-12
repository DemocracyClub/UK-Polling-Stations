from django.test import TestCase

from councils.models import Council
from data_collection.tests.stubs import stub_halaroseimport
from pollingstations.models import PollingStation, ResidentialAddress


class HalaroseImportTests(TestCase):

    opts = {
        'noclean': False,
        'nochecks': True,
        'verbosity': 0
    }

    def setUp(self):
        Council.objects.update_or_create(pk='X01000000')
        cmd = stub_halaroseimport.Command()
        cmd.handle(**self.opts)

    def test_addresses(self):
        addresses = ResidentialAddress.objects\
                                      .filter(council_id='X01000000')\
                                      .order_by('address')\
                                      .values_list('address', flat=True)

        # we should have inserted 3 addresses
        # and discarded 3 due to error conditions
        self.assertEqual(3, len(addresses))
        expected = set([
            '1 Heol Elfed, Gorseinon, Swansea',
            '47 Heol Dylan, Gorseinon, Swansea',
            '2, Dogkennel Farm Cottages',
        ])
        self.assertEqual(set(addresses), expected)

    def test_station_ids(self):
        self.assertEqual('',
            ResidentialAddress\
                .objects\
                .get(slug='x01000000-2-dogkennel-farm-cottages-ba152bb')\
                .polling_station_id
        )
        self.assertEqual('10-penyrheol-boxing-club',
            ResidentialAddress\
                .objects\
                .get(slug='x01000000-10-penyrheol-boxing-club-1-heol-elfed-gorseinon-swansea-sa44gh')\
                .polling_station_id
        )
        self.assertEqual('10-penyrheol-boxing-club',
            ResidentialAddress\
                .objects\
                .get(slug='x01000000-10-penyrheol-boxing-club-47-heol-dylan-gorseinon-swansea-sa44lr')\
                .polling_station_id
        )

    def test_stations(self):
        stations = PollingStation.objects\
                                 .filter(council_id='X01000000')\
                                 .order_by('internal_council_id')\
                                 .values_list('address', flat=True)

        # we inserted 2 stations, even though only one of them
        # had no valid addresses associated with it
        self.assertEqual(2, len(stations))
        expected = set([
            'Penyrheol Boxing Club\nGower View Road\nPenyrheol\nSwansea',
            'St Ambrose Church Hall\nWest Cliff Road\nBournemouth'
        ])
        self.assertEqual(set(stations), expected)
