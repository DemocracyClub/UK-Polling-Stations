import re
from django.apps import apps
from django.conf import settings


def get_model(const, default):
    model_str = getattr(settings, const, default)
    if not re.match('\w+\.\w+', model_str):
        raise LookupError("%s setting must be of the form 'app.Model'" % (const))
    return apps.get_model(*model_str.split('.'))

def get_address_model():
    return get_model('ADDRESS_MODEL', 'uk_geo_utils.Address')

def get_onsud_model():
    return get_model('ONSUD_MODEL', 'uk_geo_utils.Onsud')

def get_onspd_model():
    return get_model('ONSPD_MODEL', 'uk_geo_utils.Onspd')


class Postcode:

    def __init__(self, postcode, validate=False):
        self.postcode = re.sub('[^A-Z0-9]', '', str(postcode).upper())
        if validate and len(str(self.postcode)) < 5:
            raise ValueError("Postcode must have at least 5 characters")

    def __str__(self):
        return self.without_space

    def __eq__(self, other):
        return type(self) == Postcode and\
            type(other) == Postcode and\
            self.without_space == other.without_space

    @property
    def territory(self):
        if self.postcode[:2] == 'BT':
            return 'NI'
        return 'GB'

    @property
    def with_space(self):
        return self.postcode[:-3] + ' ' + self.postcode[-3:]

    @property
    def without_space(self):
        return self.postcode


class AddressFormatter:

    def __init__(
            self,
            organisation_name,
            department_name,
            po_box_number,
            sub_building_name,
            building_name,
            building_number,
            dependent_thoroughfare,
            thoroughfare,
            post_town,
            double_dependent_locality,
            dependent_locality,
            ):
        """one to one mapping."""
        self.organisation_name = organisation_name
        self.department_name = department_name
        self.po_box_number = po_box_number
        self.sub_building_name = sub_building_name
        self.building_name = building_name
        self.building_number = building_number
        self.dependent_thoroughfare = dependent_thoroughfare
        self.thoroughfare = thoroughfare
        self.post_town = post_town
        self.double_dependent_locality = double_dependent_locality
        self.dependent_locality = dependent_locality
        self.address_label = []

    def generate_address_label(self):
        """Construct a list for address label.

        Non-empty premises elements are appended to the address label in the
        order of organisation_name, department_name, po_box_number (which
        must be prepended with 'PO Box', sub_building_name, building_name,
        building_number, then the rest of the elements except for Town and
        Postcode because we want them in their own fields. This isn't strict
        address label but we're probably loading them into a database.
        """
        if self.organisation_name:
            self.address_label.append(self.organisation_name)
        if self.department_name:
            self.address_label.append(self.department_name)
        if self.po_box_number:
            self.address_label.append('PO Box ' + self.po_box_number)

        elements = [
                self.sub_building_name,
                self.building_name,
                self.building_number,
                self.dependent_thoroughfare,
                self.thoroughfare,
                self.double_dependent_locality,
                self.dependent_locality,
        ]

        for element in elements:
            if element:
                self._append_to_label(element)

        # pad label to length of 7 if not already
        if len(self.address_label) < 7:
            for i in range(7 - len(self.address_label)):
                self.address_label.append('')

        # finally, add post town
        self.address_label[5] = self.post_town

        return ", ".join([f for f in self.address_label if f])

    def _is_exception_rule(self, element):
        """ Check for "exception rule".

        Address elements will be appended onto a new line on the lable except
        for when the penultimate lable line fulfils certain criteria, in which
        case the element will be concatenated onto the penultimate line. This
        method checks for those criteria.

        i) First and last characters of the Building Name are numeric
          (eg '1to1' or '100:1')
        ii) First and penultimate characters are numeric, last character is
          alphabetic (eg '12A')
        iii) Building Name has only one character (eg 'A')
        """
        if element[0].isdigit() and element[-1].isdigit():
            return True
        if len(element) > 1 and element[0].isdigit() and element[-2].isdigit() and element[-1].isalpha():
            return True
        if len(element) == 1 and element.isalpha():
            return True
        return False

    def _append_to_label(self, element):
        """Append address element to the label.

        Normally an element will be appended onto the list, except where the
        existing last element fulfils the exception rule, in which case the
        element will be concatenated onto the final list member.
        """
        if len(self.address_label) > 0\
                and self._is_exception_rule(self.address_label[-1]):
            self.address_label[-1] += (' ' + element)
        else:
            self.address_label.append(element)

    def __str__(self):
        """Return the label form of the address."""
        return ','.join(self.generate_address_label())


class AddressSorter:
    # Class for sorting sort a list of address objects
    # in a human-readable order.

    def __init__(self, addresses):
        self.addresses = addresses

    def convert(self, text):
        # if text is numeric, covert to an int
        # this allows us to sort numbers in int order, not string order
        return int(text) if text.isdigit() else text

    def alphanum_key(self, tup):
        # split the desired component of tup (defined by key function)
        # into a listof numeric and text components
        return [ self.convert(c) for c in filter(None, re.split('([0-9]+)', tup[1])) ]

    def swap_fields(self, item):
        lst = self.alphanum_key(item)
        # swap things about so we can sort by street name, house number
        # instead of house number, street name
        if len(lst) > 1 and isinstance(lst[0], int) and isinstance(lst[1], str) and (lst[1][0].isspace() or lst[1][0] == ','):
            lst[0], lst[1] = lst[1], lst[0]
        if len(lst) > 1 and isinstance(lst[0], int) and isinstance(lst[1], int):
            lst[0], lst[1] = lst[1], lst[0]
        if isinstance(lst[0], int):
            lst[0] = str(lst[0])
        return lst

    def natural_sort(self):
        sorted_list = sorted(
            [(address, address.address) for address in self.addresses],
            key=self.swap_fields
        )
        return [address[0] for address in sorted_list]
