def centre_from_points_qs(qs):
    if not qs:
        return None

    if len(qs) == 1:
        return qs[0].location

    base_point = qs[0].location
    poly = base_point.union(qs[1].location)
    for m in qs:
        poly = poly.union(m.location)

    return poly.centroid


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
        if element[0].isdigit() and element[-2].isdigit() and element[-1].isalpha():
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
