from django.test import TestCase
from data_importers.data_types import AddressList


class MockLogger:
    def log_message(self, level, message, variable=None, pretty=False):
        pass


class AddressListTest(TestCase):
    def test_add_with_duplicates(self):
        in_list = [
            {
                "address": "foo",
                "postcode": "AA11AA",
                "council": "AAA",
                "polling_station_id": "01",
                "uprn": "1",
            },
            {
                "address": "bar",
                "postcode": "AA11AA",
                "council": "AAA",
                "polling_station_id": "01",
                "uprn": "2",
            },
            {
                "address": "foo",
                "postcode": "AA11AA",
                "council": "AAA",
                "polling_station_id": "01",
                "uprn": "1",
            },
        ]

        expected = [
            {
                "address": "foo",
                "postcode": "AA11AA",
                "council": "AAA",
                "polling_station_id": "01",
                "uprn": "1",
            },
            {
                "address": "bar",
                "postcode": "AA11AA",
                "council": "AAA",
                "polling_station_id": "01",
                "uprn": "2",
            },
            {  # This is correct we deal with duplicates later.
                "address": "foo",
                "postcode": "AA11AA",
                "council": "AAA",
                "polling_station_id": "01",
                "uprn": "1",
            },
        ]

        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)

        self.assertEqual(expected, address_list.elements)

    def test_get_uprn_lookup(self):
        in_list = [
            {
                "polling_station_id": "01",
                "address": "foo 1",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "1",
            },
            {
                "polling_station_id": "01",
                "address": "foo 2",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "2",
            },
            {
                "polling_station_id": "01",
                "address": "foo 3",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "3",
            },
            {
                "polling_station_id": "02",
                "address": "foo 4",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "4",
            },
            {
                "polling_station_id": "02",
                "address": "foo 5",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "5",
            },
            {
                "polling_station_id": "01",
                "address": "foo 5",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "5",
            },
        ]
        expected = {
            "1": {"01"},
            "2": {"01"},
            "3": {"01"},
            "4": {"02"},
            "5": {"02", "01"},
        }
        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)

        self.assertEqual(expected, address_list.get_uprn_lookup())

    def test_remove_duplicate_uprns(self):
        in_list = [
            {
                "polling_station_id": "01",
                "address": "foo 1",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "1",
            },
            {
                "polling_station_id": "01",
                "address": "foo 2",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "2",
            },
            {
                "polling_station_id": "01",
                "address": "foo 3",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "3",
            },
            {
                "polling_station_id": "02",
                "address": "foo 4",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "4",
            },
            {
                "polling_station_id": "02",
                "address": "foo 5",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "5",
            },
            {
                "polling_station_id": "01",
                "address": "foo 5",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "5",
            },
        ]

        expected = [
            {
                "polling_station_id": "01",
                "address": "foo 1",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "1",
            },
            {
                "polling_station_id": "01",
                "address": "foo 2",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "2",
            },
            {
                "polling_station_id": "01",
                "address": "foo 3",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "3",
            },
            {
                "polling_station_id": "02",
                "address": "foo 4",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "4",
            },
        ]
        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)

        address_list.remove_duplicate_uprns()
        self.assertEqual(expected, address_list.elements)

    def test_get_polling_station_lookup(self):
        in_list = [
            {
                "polling_station_id": "01",
                "address": "foo 1",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "1",
            },
            {
                "polling_station_id": "01",
                "address": "foo 2",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "2",
            },
            {
                "polling_station_id": "01",
                "address": "foo 3",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "3",
            },
            {
                "polling_station_id": "02",
                "address": "foo 4",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "4",
            },
        ]
        expected = {
            "01": {
                "1",
                "2",
                "3",
            },
            "02": {"4"},
        }
        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)

        self.assertEqual(expected, address_list.get_polling_station_lookup())

    def test_remove_records_not_in_addressbase(self):
        in_list = [
            {
                "polling_station_id": "01",
                "address": "foo 1",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "1",
            },
            {
                "polling_station_id": "01",
                "address": "foo 2",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "2",
            },
        ]
        addressbase_data = {"1": {"postcode": "AA1 2BB"}}
        expected = [
            {
                "polling_station_id": "01",
                "address": "foo 1",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "1",
            },
        ]

        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)

        address_list.remove_records_not_in_addressbase(addressbase_data)
        self.assertEqual(expected, address_list.elements)

    def test_remove_records_that_dont_match_addressbase(self):
        in_list = [
            {
                "polling_station_id": "01",
                "address": "foo 1",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "1",
            },
            {
                "polling_station_id": "01",
                "address": "foo 2",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "2",
            },
        ]
        addressbase_data = {"1": {"postcode": "AA1 2BB"}, "2": {"postcode": "AA1 2CC"}}
        expected = [
            {
                "polling_station_id": "01",
                "address": "foo 1",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "1",
            },
        ]

        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)

        address_list.remove_records_that_dont_match_addressbase(addressbase_data)
        self.assertEqual(expected, address_list.elements)

    def test_check_records(self):
        pass
