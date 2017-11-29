from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from data_finder.helpers import (
    AddressBaseGeocoderAdapter, MultipleCouncilsException)
from uk_geo_utils.geocoders import (
    AddressBaseGeocoder,
    CodesNotFoundException
)


class AddressBaseGeocoderAdapterTest(TestCase):

    fixtures = ['test_addressbase.json']

    def test_no_records(self):
        """
        We can't find any records for the given postcode in the AddressBase table

        Exception of class ObjectDoesNotExist should be thrown
        """
        addressbase = AddressBaseGeocoderAdapter('DD1 1DD')
        with self.assertRaises(ObjectDoesNotExist):
            result = addressbase.geocode()

        # point only geocode should also fail
        with self.assertRaises(ObjectDoesNotExist):
            result = addressbase.geocode_point_only()

    def test_no_codes(self):
        """
        We find records for the given postcode in the AddressBase table
        but there are no corresponding records in the ONSUD for the UPRNs we found

        Exception of class CodesNotFoundException should be thrown
        """
        addressbase = AddressBaseGeocoderAdapter('AA11AA')
        with self.assertRaises(CodesNotFoundException):
            result = addressbase.geocode()

        # point only geocode should return a result anyway
        result = addressbase.geocode_point_only()
        self.assertIsInstance(result, AddressBaseGeocoder)

    def test_multiple_councils(self):
        """
        We find records for the given postcode in the AddressBase table
        There are corresponding records in the ONSUD for the UPRNs we found
        The UPRNs described by this postcode map to more than one local authority

        Exception of class MultipleCouncilsException should be thrown
        """
        addressbase = AddressBaseGeocoderAdapter('CC11CC')
        with self.assertRaises(MultipleCouncilsException):
            result = addressbase.geocode()

        # point only geocode should return a result anyway
        result = addressbase.geocode_point_only()
        self.assertIsInstance(result, AddressBaseGeocoder)

    def test_valid(self):
        """
        We find records for the given postcode in the AddressBase table
        There are some corresponding records in the ONSUD for the UPRNs we found

        Valid result should be returned

        Note that in this case, the ONSUD table does not contain corresponding
        records for *all* of the UPRNs we found, but we accept the result anyway
        """
        addressbase = AddressBaseGeocoderAdapter('bb 1   1B B')  # intentionally spurious whitespace and case
        result = addressbase.geocode()
        self.assertIsInstance(result, AddressBaseGeocoder)
        self.assertEqual('B01000001', result.get_code('lad'))
