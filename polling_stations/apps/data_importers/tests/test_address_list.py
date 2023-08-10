from addressbase.tests.factories import AddressFactory
from data_importers.data_types import AddressList
from django.test import TestCase


class MockLogger:
    logs = []

    def log_message(self, level, message, variable=None, pretty=False):
        self.logs.append(message)

    def clear_logs(self):
        self.logs = []


class AddressListTest(TestCase):
    def test_append(self):
        in_list = [
            {
                "address": "foo",
                "postcode": "AA11AA",
                "council": "AAA",
                "polling_station_id": "01",
                "uprn": "1",
            },
            {  # Doesn't need a uprn - this should be added
                "address": "bar",
                "postcode": "AA11AA",
                "council": "AAA",
                "polling_station_id": "01",
                "uprn": "",
            },
            {  # Does need a postcode - this shouldn't
                "address": "baz",
                "postcode": "",
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
                "uprn": "",
            },
        ]
        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)

        self.assertEqual(expected, address_list.elements)

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
                "uprn": "01",
            },
            {
                "polling_station_id": "01",
                "address": "foo 2",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "02",
            },
            {
                "polling_station_id": "01",
                "address": "foo 3",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "03",
            },
            {
                "polling_station_id": "02",
                "address": "foo 4",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "04",
            },
        ]
        expected = {
            "01": {
                "01",
                "02",
                "03",
            },
            "02": {"04"},
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

    def test_remove_records_that_dont_match_addressbase_with_duplicates(self):
        in_list = [
            {
                "polling_station_id": "01",
                "address": "foo 1",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "10",
            },
            {
                "polling_station_id": "01",
                "address": "foo 2",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "20",
            },
            {
                "polling_station_id": "01",
                "address": "foo 2",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "20",
            },
        ]
        addressbase_data = {
            "10": {"postcode": "AA1 2BB"},
            "20": {"postcode": "AA1 2CC"},
        }
        expected = [
            {
                "polling_station_id": "01",
                "address": "foo 1",
                "postcode": "AA1 2BB",
                "council": "AAA",
                "uprn": "10",
            },
        ]

        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)
        address_list.remove_records_that_dont_match_addressbase(addressbase_data)
        self.assertEqual(expected, address_list.elements)

    def test_get_council_split_postcodes(self):
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
                "polling_station_id": "02",
                "uprn": "2",
            },
            {
                "address": "baz",
                "postcode": "BB11BB",
                "council": "AAA",
                "polling_station_id": "03",
                "uprn": "1",
            },
        ]

        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)
        expected = ["AA11AA"]
        self.assertListEqual(expected, address_list.get_council_split_postcodes())

    def test_remove_records_missing_uprns(self):
        in_list = [
            {
                "address": "foo",
                "postcode": "AA11AA",
                "council": "AAA",
                "polling_station_id": "01",
                "uprn": "1",
            },
            {  # Doesn't need a uprn - this should be added
                "address": "bar",
                "postcode": "AA11AA",
                "council": "AAA",
                "polling_station_id": "01",
                "uprn": "",
            },
            {  # Does need a postcode - this shouldn't
                "address": "baz",
                "postcode": "",
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
        ]
        address_list = AddressList(MockLogger())
        for el in in_list:
            address_list.append(el)
        address_list.remove_records_missing_uprns()
        self.assertEqual(expected, address_list.elements)

    def test_check_split_postcodes_are_split(self):
        """
        AddressBase                      | Council Data
                                         |
        uprn | Address        | Postcode | uprn | Address       | Postcode | Station
        ---------------------------------|------------------------------------------
        123  | 1 Foo Street   | AA11AA   | 123  | 1 Foo Street  | AA11AA   | A1
        124  | 2 Foo Street   | AA11AA   | 124  | 2 Foo Street  | AA11AA   | A1
        125  | 3 Foo Street   | AA11AA   | 125  | 3 Foo Street  | AA22AA   | A2
        ---------------------------------|------------------------------------------
        223  | 1 Bar Street   | BB11BB   | 223  | 1 Bar Street  | BB11BB   | B1
        224  | 2 Bar Street   | BB11BB   | 224  | 2 Bar Street  | BB11BB   | B1
                                         | 225  | 3 Bar Street  | BB11BB   | B2
        ---------------------------------|------------------------------------------
        323  | 1 Baz Street   | CC11CC   | 323  | 1 Baz Street  | CC11CC   | C1
        324  | 2 Baz Street   | CC11CC   | 324  | 2 Baz Street  | CC11CC   | C1
        325  | 3 Baz Street   | CC22CC   | 325  | 3 Baz Street  | CC11CC   | C2

        BB11BB and CC11CC are the ones we won't think are split, but are really.
        Our checks should remove 225 and 325 because there aren't matches for them
        in addressbase. Therefore they're not in the in_list.
        """

        in_list = [
            {
                "address": "1 Foo Street",
                "postcode": "AA11AA",
                "council": "AAA",
                "polling_station_id": "A1",
                "uprn": "123",
            },
            {
                "address": "2 Foo Street",
                "postcode": "AA11AA",
                "council": "AAA",
                "polling_station_id": "A1",
                "uprn": "124",
            },
            {
                "address": "3 Foo Street",
                "postcode": "AA22AA",
                "council": "AAA",
                "polling_station_id": "A2",
                "uprn": "125",
            },
            {
                "address": "1 Bar Street",
                "postcode": "BB11BB",
                "council": "AAA",
                "polling_station_id": "B1",
                "uprn": "223",
            },
            {
                "address": "2 Bar Street",
                "postcode": "BB11BB",
                "council": "AAA",
                "polling_station_id": "B1",
                "uprn": "224",
            },
            {
                "address": "1 Baz Street",
                "postcode": "CC11CC",
                "council": "AAA",
                "polling_station_id": "C1",
                "uprn": "323",
            },
            {
                "address": "2 Baz Street",
                "postcode": "CC11CC",
                "council": "AAA",
                "polling_station_id": "C1",
                "uprn": "324",
            },
        ]

        addressbase = [
            # AA11A
            {"uprn": "123", "address": "1 Foo Street", "postcode": "AA11AA"},
            {"uprn": "124", "address": "2 Foo Street", "postcode": "AA11AA"},
            {"uprn": "125", "address": "3 Foo Street", "postcode": "AA11AA"},
            # BB11BB
            {"uprn": "223", "address": "1 Bar Street ", "postcode": "BB11BB"},
            {"uprn": "224", "address": "2 Bar Street ", "postcode": "BB11BB"},
            # CC11CC
            {"uprn": "323", "address": "1 Baz Street", "postcode": "CC11CC"},
            {"uprn": "324", "address": "2 Baz Street", "postcode": "CC11CC"},
            # CC22CC
            {"uprn": "325", "address": "3 Baz Street", "postcode": "CC22CC"},
        ]
        for address in addressbase:
            AddressFactory(**address)
        address_list = AddressList(MockLogger())
        address_list.logger.clear_logs()
        for el in in_list:
            address_list.append(el)

        split_postcodes = ["BB11BB", "CC11CC"]
        address_list.check_split_postcodes_are_split(split_postcodes)
        self.assertListEqual(
            address_list.logger.logs,
            [
                'These postcodes are split in council data: "BB11BB", "CC11CC", but won\'t be in the db once imported.'
            ],
        )

    def test_check_records(self):
        pass
