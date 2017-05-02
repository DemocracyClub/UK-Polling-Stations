import mock
from django.test import TestCase
from data_finder.helpers import EveryElectionWrapper


# mock get_data() functions
def get_data_exception(self, postcode):
    raise Exception()

def get_data_no_elections(self, postcode):
    return []

def get_data_with_elections(self, postcode):
    return [
        {'election_title': 'some election'},  # no explanation key
        {'election_title': 'some election', 'explanation': None},  # null explanation key
        {'election_title': 'some election', 'explanation': 'some text'},  # explanation key contains text
    ]

class EveryElectionWrapperTest(TestCase):

    @mock.patch("data_finder.helpers.EveryElectionWrapper.get_data", get_data_exception)
    def test_exception(self):
        ee = EveryElectionWrapper('AA11AA')
        self.assertFalse(ee.request_success)
        self.assertTrue(ee.has_election())
        self.assertEqual([], ee.get_explanations())

    @mock.patch("data_finder.helpers.EveryElectionWrapper.get_data", get_data_no_elections)
    def test_no_elections(self):
        ee = EveryElectionWrapper('AA11AA')
        self.assertTrue(ee.request_success)
        self.assertFalse(ee.has_election())
        self.assertEqual([], ee.get_explanations())

    @mock.patch("data_finder.helpers.EveryElectionWrapper.get_data", get_data_with_elections)
    def test_elections(self):
        ee = EveryElectionWrapper('AA11AA')
        self.assertTrue(ee.request_success)
        self.assertTrue(ee.has_election())
        self.assertEqual([
            {'title': 'some election', 'explanation': 'some text'}
        ], ee.get_explanations())
