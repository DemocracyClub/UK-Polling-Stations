# -*- coding: utf-8 -*-
from django.test import TestCase
from uk_geo_utils.helpers import Postcode

class PostcodeHelperTest(TestCase):

    postcodes = [
        {
            'input':        'm1+1Aa',
            'exp_space':    'M1 1AA',
            'exp_no_space': 'M11AA'
        },
        {
            'input':        'm60�1nw',
            'exp_space':    'M60 1NW',
            'exp_no_space': 'M601NW'
        },
        {
            'input':        'cR26xh        ',
            'exp_space':    'CR2 6XH',
            'exp_no_space': 'CR26XH'
        },
        {
            'input':        'dn55      1pt',
            'exp_space':    'DN55 1PT',
            'exp_no_space': 'DN551PT'
        },
        {
            'input':        'w1a1hq',
            'exp_space':    'W1A 1HQ',
            'exp_no_space': 'W1A1HQ'
        },
        {
            'input':        'e;C1,,a1b&=-^£%b',
            'exp_space':    'EC1A 1BB',
            'exp_no_space': 'EC1A1BB'
        },
    ]

    def test_with_spaces(self):
        for postcode in self.postcodes:
            self.assertEqual(
                postcode['exp_space'],
                Postcode(postcode['input']).with_space
            )

    def test_without_spaces(self):
        for postcode in self.postcodes:
            self.assertEqual(
                postcode['exp_no_space'],
                Postcode(postcode['input']).without_space
            )

    def test_equality_equal(self):
        self.assertEqual(Postcode('AA1 1AA'), Postcode('AA11AA'))

    def test_equality_not_equal(self):
        self.assertNotEqual(Postcode('AA1 1AA'), Postcode('AA1 1AB'))

    def test_equality_different_type(self):
        self.assertNotEqual('AA1 1AA', Postcode('AA1 1AA'))
