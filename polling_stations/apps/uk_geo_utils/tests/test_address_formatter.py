from django.test import TestCase
from uk_geo_utils.helpers import AddressFormatter

class AddressFormatterTest(TestCase):

    def test_common_address(self):
        af = AddressFormatter(
            organisation_name='',
            department_name='',
            po_box_number='',
            sub_building_name='',
            building_name='',
            building_number='33',
            dependent_thoroughfare='',
            thoroughfare='BONEHURST ROAD',
            post_town='HORLEY',
            double_dependent_locality='',
            dependent_locality='',
        )
        self.assertEqual(
            '33 BONEHURST ROAD, HORLEY',
            af.generate_address_label()
        )

    def test_building_name_x_to_y(self):
        af = AddressFormatter(
            organisation_name='MELA',
            department_name='',
            po_box_number='',
            sub_building_name='',
            building_name='1-7',
            building_number='',
            dependent_thoroughfare='',
            thoroughfare='LINKFIELD STREET',
            post_town='REDHILL',
            double_dependent_locality='',
            dependent_locality='',
        )
        self.assertEqual(
            'MELA, 1-7 LINKFIELD STREET, REDHILL',
            af.generate_address_label()
        )

    def test_building_name_suffix(self):
        af = AddressFormatter(
            organisation_name='',
            department_name='',
            po_box_number='',
            sub_building_name='',
            building_name='2A',
            building_number='',
            dependent_thoroughfare='',
            thoroughfare='MANOR ROAD',
            post_town='TAMWORTH',
            double_dependent_locality='',
            dependent_locality='MILE OAK',
        )
        self.assertEqual(
            '2A MANOR ROAD, MILE OAK, TAMWORTH',
            af.generate_address_label()
        )

    def test_sub_building_name(self):
        af = AddressFormatter(
            organisation_name='',
            department_name='',
            po_box_number='',
            sub_building_name='FLAT 12',
            building_name='GLOBE COURT',
            building_number='',
            dependent_thoroughfare='',
            thoroughfare='HIGH ROAD',
            post_town='BROXBOURNE',
            double_dependent_locality='',
            dependent_locality='',
        )
        self.assertEqual(
            'FLAT 12, GLOBE COURT, HIGH ROAD, BROXBOURNE',
            af.generate_address_label()
        )

    def test_org_and_dept(self):
        af = AddressFormatter(
            organisation_name='INVERCLYDE COUNCIL',
            department_name='TRANSPORT & CLEANSING',
            po_box_number='',
            sub_building_name='',
            building_name='',
            building_number='10',
            dependent_thoroughfare='',
            thoroughfare='POTTERY STREET',
            post_town='GREENOCK',
            double_dependent_locality='',
            dependent_locality='',
        )
        self.assertEqual(
            'INVERCLYDE COUNCIL, TRANSPORT & CLEANSING, 10 POTTERY STREET, GREENOCK',
            af.generate_address_label()
        )

    def test_po_box(self):
        af = AddressFormatter(
            organisation_name='AKZO NOBEL CAR REFINISHES BV',
            department_name='',
            po_box_number='3986',
            sub_building_name='',
            building_name='',
            building_number='',
            dependent_thoroughfare='',
            thoroughfare='',
            post_town='SWINDON',
            double_dependent_locality='',
            dependent_locality='',
        )
        self.assertEqual(
            'AKZO NOBEL CAR REFINISHES BV, PO Box 3986, SWINDON',
            af.generate_address_label()
        )
