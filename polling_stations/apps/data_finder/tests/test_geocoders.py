import mock
from django.test import TestCase
from data_finder.helpers import (
    geocode, geocode_point_only, MapitGeocoder, MultipleCouncilsException
)


"""
Mock out a stub response from mapit
we don't really care about the actual data for these tests
just where it came from
"""
def mock_geocode(self):
    return { 'source': 'mapit' }


class GeocodeTest(TestCase):

    fixtures = ['test_addressbase.json']

    @mock.patch("data_finder.helpers.MapitGeocoder.geocode", mock_geocode)
    def test_no_records(self):
        """
        We can't find any records for the given postcode in the AddressBase table

        We should fall back to centroid-based geocoding using mapit
        """
        result = geocode('DD1 1DD')
        self.assertEqual('mapit', result['source'])

    @mock.patch("data_finder.helpers.MapitGeocoder.geocode", mock_geocode)
    def test_no_codes(self):
        """
        We find records for the given postcode in the AddressBase table
        but there are no corresponding records in the ONSAD for the UPRNs we found

        We should fall back to centroid-based geocoding using mapit
        """
        result = geocode('AA11AA')
        self.assertEqual('mapit', result['source'])

    @mock.patch("data_finder.helpers.MapitGeocoder.geocode", mock_geocode)
    def test_multiple_councils(self):
        """
        We find records for the given postcode in the AddressBase table
        There are corresponding records in the ONSAD for the UPRNs we found
        The UPRNs described by this postcode map to more than one local authority

        Exception of class MultipleCouncilsException should be thrown
        """
        exception_thrown = False
        try:
            result = geocode('CC11CC')
        except MultipleCouncilsException:
            exception_thrown = True
        self.assertTrue(exception_thrown)

    @mock.patch("data_finder.helpers.MapitGeocoder.geocode", mock_geocode)
    def test_valid(self):
        """
        We find records for the given postcode in the AddressBase table
        There are some corresponding records in the ONSAD for the UPRNs we found

        Valid result should be returned based on geocoding using AddressBase
        """
        result = geocode('BB1 1BB')
        self.assertEqual('addressbase', result['source'])


class GeocodePointOnlyTest(TestCase):

    fixtures = ['test_addressbase.json']

    @mock.patch("data_finder.helpers.MapitGeocoder.geocode", mock_geocode)
    def test_no_records(self):
        """
        We can't find any records for the given postcode in the AddressBase table

        We should fall back to centroid-based geocoding using mapit
        """
        result = geocode_point_only('DD1 1DD', sleep=False)
        self.assertEqual('mapit', result['source'])

    @mock.patch("data_finder.helpers.MapitGeocoder.geocode", mock_geocode)
    def test_valid(self):
        """
        We find records for the given postcode in the AddressBase table
        There are some corresponding records in the ONSAD for the UPRNs we found

        Valid result should be returned based on geocoding using AddressBase
        """
        result = geocode_point_only('BB1 1BB', sleep=False)
        self.assertEqual('addressbase', result['source'])
