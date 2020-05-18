import mock
from django.test import TestCase, override_settings
from data_finder.helpers.geocoders import (
    geocode,
    geocode_point_only,
)
from uk_geo_utils.geocoders import (
    AddressBaseGeocoder,
    OnspdGeocoder,
    MultipleCodesException,
)


class StubOnspdGeocoder(OnspdGeocoder):
    def __init__(self, postcode):
        pass


"""
Mock out a stub response from OnspdGeocoder
we don't really care about the actual data for these tests
just where it came from
"""


def mock_geocode(self, uprn=None):
    return StubOnspdGeocoder("foo")


class GeocodeTest(TestCase):

    fixtures = ["test_addressbase.json"]

    @mock.patch(
        "data_finder.helpers.geocoders.OnspdGeocoderAdapter.geocode", mock_geocode
    )
    def test_no_records(self):
        """
        We can't find any records for the given postcode in the AddressBase table

        We should fall back to centroid-based geocoding using ONSPD
        """
        result = geocode("DD1 1DD")
        self.assertIsInstance(result, OnspdGeocoder)

    @mock.patch(
        "data_finder.helpers.geocoders.OnspdGeocoderAdapter.geocode", mock_geocode
    )
    def test_no_codes(self):
        """
        We find records for the given postcode in the AddressBase table
        but there are no corresponding records in the uprn to council lookup
        for the UPRNs we found

        We should fall back to centroid-based geocoding using ONSPD
        """
        result = geocode("AA11AA")
        self.assertIsInstance(result, OnspdGeocoder)

    @mock.patch(
        "data_finder.helpers.geocoders.OnspdGeocoderAdapter.geocode", mock_geocode
    )
    def test_multiple_councils(self):
        """
        We find records for the given postcode in the AddressBase table
        There are corresponding records in the uprn to council lookup
        for the UPRNs we found
        The UPRNs described by this postcode map to more than one local authority

        Exception of class MultipleCodesException should be thrown
        """
        with self.assertRaises(MultipleCodesException):
            geocode("CC11CC")

    @mock.patch(
        "data_finder.helpers.geocoders.OnspdGeocoderAdapter.geocode", mock_geocode
    )
    def test_valid(self):
        """
        We find records for the given postcode in the AddressBase table
        There are some corresponding records in the uprn to council lookup
        for the UPRNs we found

        Valid result should be returned based on geocoding using AddressBase
        """
        result = geocode("BB1 1BB")
        self.assertIsInstance(result, AddressBaseGeocoder)

    @mock.patch(
        "data_finder.helpers.geocoders.OnspdGeocoderAdapter.geocode", mock_geocode
    )
    @override_settings(OLD_TO_NEW_MAP={"B01000001": "fake temp gss code"})
    def test_manual_pverride(self):
        result = geocode("BB1 1BB")
        self.assertEqual(result.get_code("lad"), "fake temp gss code")


class GeocodePointOnlyTest(TestCase):

    fixtures = ["test_addressbase.json"]

    @mock.patch(
        "data_finder.helpers.geocoders.OnspdGeocoderAdapter.geocode_point_only",
        mock_geocode,
    )
    def test_no_records(self):
        """
        We can't find any records for the given postcode in the AddressBase table

        We should fall back to centroid-based geocoding using ONSPD
        """
        result = geocode_point_only("DD1 1DD")
        self.assertIsInstance(result, OnspdGeocoder)

    @mock.patch(
        "data_finder.helpers.geocoders.OnspdGeocoderAdapter.geocode_point_only",
        mock_geocode,
    )
    def test_valid(self):
        """
        We find records for the given postcode in the AddressBase table
        There are some corresponding records in the uprn to council lookup
        for the UPRNs we found

        Valid result should be returned based on geocoding using AddressBase
        """
        result = geocode_point_only("BB1 1BB")
        self.assertIsInstance(result, AddressBaseGeocoder)
