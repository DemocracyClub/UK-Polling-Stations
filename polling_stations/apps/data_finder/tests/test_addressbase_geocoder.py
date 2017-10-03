from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from data_finder.helpers import (
    AddressBaseGeocoder, CodesNotFoundException, MultipleCouncilsException
)


class AddressBaseGeocoderTest(TestCase):

    fixtures = ['test_addressbase.json']

    def test_no_records(self):
        """
        We can't find any records for the given postcode in the AddressBase table

        Exception of class ObjectDoesNotExist should be thrown
        """
        addressbase = AddressBaseGeocoder('DD1 1DD')
        exception_thrown = False
        try:
            result = addressbase.geocode()
        except ObjectDoesNotExist:
            exception_thrown = True
        self.assertTrue(exception_thrown)

        # point only geocode should also fail
        try:
            result = addressbase.geocode_point_only()
        except ObjectDoesNotExist:
            exception_thrown = True
        self.assertTrue(exception_thrown)

    def test_no_codes(self):
        """
        We find records for the given postcode in the AddressBase table
        but there are no corresponding records in the ONSUD for the UPRNs we found

        Exception of class CodesNotFoundException should be thrown
        """
        addressbase = AddressBaseGeocoder('AA11AA')
        exception_thrown = False
        try:
            result = addressbase.geocode()
        except CodesNotFoundException:
            exception_thrown = True
        self.assertTrue(exception_thrown)

        # point only geocode should return a result anyway
        result = addressbase.geocode_point_only()
        self.assertEqual('addressbase', result['source'])

    def test_multiple_councils(self):
        """
        We find records for the given postcode in the AddressBase table
        There are corresponding records in the ONSUD for the UPRNs we found
        The UPRNs described by this postcode map to more than one local authority

        Exception of class MultipleCouncilsException should be thrown
        """
        addressbase = AddressBaseGeocoder('CC11CC')
        exception_thrown = False
        try:
            result = addressbase.geocode()
        except MultipleCouncilsException:
            exception_thrown = True
        self.assertTrue(exception_thrown)

        # point only geocode should return a result anyway
        result = addressbase.geocode_point_only()
        self.assertEqual('addressbase', result['source'])

    def test_valid(self):
        """
        We find records for the given postcode in the AddressBase table
        There are some corresponding records in the ONSUD for the UPRNs we found

        Valid result should be returned

        Note that in this case, the ONSUD table does not contain corresponding
        records for *all* of the UPRNs we found, but we accept the result anyway
        """
        addressbase = AddressBaseGeocoder('bb 1   1B B')  # intentionally spurious whitespace and case
        result = addressbase.geocode()
        self.assertEqual('addressbase', result['source'])
        self.assertEqual('B01000001', result['council_gss'])
