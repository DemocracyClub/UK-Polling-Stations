from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from data_finder.helpers.geocoders import AddressBaseGeocoderAdapter
from uk_geo_utils.geocoders import (
    AddressBaseGeocoder,
    CodesNotFoundException,
    MultipleCodesException,
)


class AddressBaseGeocoderAdapterTest(TestCase):

    fixtures = ["test_addressbase.json"]

    def test_no_records(self):
        """
        We can't find any records for the given postcode in the AddressBase table

        Exception of class ObjectDoesNotExist should be thrown
        """
        addressbase = AddressBaseGeocoderAdapter("DD1 1DD")
        with self.assertRaises(ObjectDoesNotExist):
            addressbase.geocode()

        # point only geocode should also fail
        with self.assertRaises(ObjectDoesNotExist):
            addressbase.geocode_point_only()

    def test_no_codes(self):
        """
        We find records for the given postcode in the AddressBase table
        but there are no corresponding records in the uprn to council lookup
        for the UPRNs we found

        Exception of class CodesNotFoundException should be thrown
        """
        addressbase = AddressBaseGeocoderAdapter("AA11AA")
        with self.assertRaises(CodesNotFoundException):
            result = addressbase.geocode()

        # point only geocode should return a result anyway
        result = addressbase.geocode_point_only()
        self.assertIsInstance(result, AddressBaseGeocoder)

    def test_multiple_councils(self):
        """
        We find records for the given postcode in the AddressBase table
        There are corresponding records in the uprn Lookup table for the
        UPRNs we found.
        The UPRNs described by this postcode map to more than one local authority

        Result should be different depending on uprn
        """
        addressbase = AddressBaseGeocoderAdapter("CC11CC")

        # geocode postcode intersecting with more than one council should raise
        with self.assertRaises(MultipleCodesException):
            addressbase.geocode()

        # geocode method should work with a uprn
        result_00000008 = addressbase.geocode(uprn="00000008")
        result_00000009 = addressbase.geocode(uprn="00000009")
        self.assertIsInstance(result_00000008, AddressBaseGeocoder)
        self.assertIsInstance(result_00000009, AddressBaseGeocoder)

        # point only geocode should return a result anyway
        result_point_only = addressbase.geocode_point_only()
        self.assertIsInstance(result_point_only, AddressBaseGeocoder)

    def test_valid(self):
        """
        We find records for the given postcode in the AddressBase table
        There are some corresponding records in the uprn to council lookup
        for the UPRNs we found

        Valid result should be returned

        Note that in this case, the uprn to council lookup table does not contain
        corresponding records for *all* of the UPRNs we found, but we accept the
        result anyway
        """
        addressbase = AddressBaseGeocoderAdapter(
            "bb 1   1B B"
        )  # intentionally spurious whitespace and case
        result = addressbase.geocode()
        self.assertIsInstance(result, AddressBaseGeocoder)
        self.assertEqual("B01000001", result.get_code("lad"))
