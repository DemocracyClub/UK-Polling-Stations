from django.test import TestCase, override_settings
from django.core.exceptions import FieldDoesNotExist
from django.contrib.gis.geos import Point
from uk_geo_utils.geocoders import (
    AddressBaseGeocoder,
    get_address_model,
    get_onsud_model,
    AddressBaseNotImportedException,
    CodesNotFoundException,
    MultipleCodesException,
    NorthernIrelandException,
)


# TODO: This override can be removed when you spin this
# out into a seperate package. It is only needed because
# we're running the tests inside WhereDIV as a host app
@override_settings(ADDRESS_MODEL='uk_geo_utils.Address')
class AddressBaseGeocoderTest(TestCase):

    fixtures = [
        # records in Address, no corresponding records in ONSUD
        'addressbase_geocoder/AA11AA.json',

        # 3 records in Address, 2 corresponding records in ONSUD
        # all in county A01000001 and local auth B01000001
        'addressbase_geocoder/BB11BB.json',

        # records in Address, corresponding records in ONSUD
        # all in county A01000001 but split across
        # local auths B01000001 and B01000002
        'addressbase_geocoder/CC11CC.json',
    ]

    def test_empty_table(self):
        """
        The AddressBase table has no records in it
        """
        get_address_model().objects.all().delete()
        with self.assertRaises(AddressBaseNotImportedException):
            addressbase = AddressBaseGeocoder('AA11AA')

    def test_northern_ireland(self):
        with self.assertRaises(NorthernIrelandException):
            addressbase = AddressBaseGeocoder('BT11AA')

    def test_no_records(self):
        """
        We can't find any records for the given postcode in the AddressBase table
        """
        with self.assertRaises(get_address_model().DoesNotExist):
            addressbase = AddressBaseGeocoder('ZZ1 1ZZ')

    def test_no_codes(self):
        """
        We find records for the given postcode in the AddressBase table
        but there are no corresponding records in the ONSUD for the UPRNs we found
        """
        addressbase = AddressBaseGeocoder('AA11AA')

        with self.assertRaises(CodesNotFoundException):
            result = addressbase.get_code('lad')

        self.assertIsInstance(addressbase.centroid, Point)

    def test_valid(self):
        """
        We find records for the given postcode in the AddressBase table
        There are some corresponding records in the ONSUD for the UPRNs we found

        Valid result should be returned

        Note that in this case, the ONSUD table does not contain corresponding
        records for *all* of the UPRNs we found, but we accept the result anyway
        """
        addressbase = AddressBaseGeocoder('bb 1   1B B')  # intentionally spurious whitespace and case
        self.assertEqual('B01000001', addressbase.get_code('lad'))
        self.assertIsInstance(addressbase.centroid, Point)

    def test_multiple_codes(self):
        """
        We find records for the given postcode in the AddressBase table
        There are corresponding records in the ONSUD for the UPRNs we found
        The UPRNs described by this postcode map to more than one 'lad'
        but they all map to the same 'cty'
        """
        addressbase = AddressBaseGeocoder('CC1 1CC')

        with self.assertRaises(MultipleCodesException):
            result = addressbase.get_code('lad')

        self.assertEqual('A01000001', addressbase.get_code('cty'))

        self.assertIsInstance(addressbase.centroid, Point)

    def test_invalid_code_type(self):
        addressbase = AddressBaseGeocoder('CC1 1CC')
        with self.assertRaises(FieldDoesNotExist):
            result = addressbase.get_code('foo')  # not a real code type

    def test_get_code_by_uprn_valid(self):
        """
        valid get_code() by UPRN queries
        """
        addressbase = AddressBaseGeocoder('CC1 1CC')
        self.assertEqual('B01000001', addressbase.get_code('lad', '00000008'))
        self.assertEqual('B01000002', addressbase.get_code('lad', '00000009'))

    def test_get_code_by_uprn_invalid_uprn(self):
        """
        'foo' is not a valid UPRN in our DB
        """
        addressbase = AddressBaseGeocoder('CC1 1CC')
        with self.assertRaises(get_address_model().DoesNotExist):
            result = addressbase.get_code('lad', 'foo')

    def test_get_code_by_uprn_invalid_uprn_for_postcode(self):
        """
        '00000001' is a valid UPRN in our DB,
        but for a different postcode
        than the one we constructed with
        """
        addressbase = AddressBaseGeocoder('CC1 1CC')
        with self.assertRaises(get_address_model().DoesNotExist):
            result = addressbase.get_code('lad', '00000001')

    def test_get_code_by_uprn_no_onsud(self):
        """
        '00000006' is a valid UPRN in AddressBase but not in ONSUD
        """
        addressbase = AddressBaseGeocoder('BB1 1BB')
        with self.assertRaises(get_onsud_model().DoesNotExist):
            result = addressbase.get_code('lad', '00000006')
