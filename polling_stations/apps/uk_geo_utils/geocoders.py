import abc
from django.core.exceptions import ObjectDoesNotExist
from uk_geo_utils.helpers import (
    get_address_model, get_onsud_model, Postcode)


class CodesNotFoundException(Exception):
    pass

class MultipleCodesException(Exception):
    pass

class NorthernIrelandException(ObjectDoesNotExist):
    pass

class AddressBaseNotImportedException(ObjectDoesNotExist):
    pass


class BaseGeocoder(metaclass=abc.ABCMeta):

    def __init__(self, postcode):
        self.postcode = Postcode(postcode)

    @property
    @abc.abstractmethod
    def centroid(self):
        pass

    @abc.abstractmethod
    def get_code(code_type, uprn=None):
        pass


class AddressBaseGeocoder(BaseGeocoder):

    def __init__(self, postcode):

        self.postcode = Postcode(postcode)
        if self.postcode.territory == 'NI':
            raise NorthernIrelandException('Postcode is in Northern Ireland')

        self.onsud_model = get_onsud_model()
        self.address_model = get_address_model()

        try:
            # check if there are one or more records in the address table
            self.address_model.objects.raw(
                "SELECT uprn FROM %s LIMIT 1;" %\
                (self.address_model._meta.db_table))[0]
        except IndexError:
            raise AddressBaseNotImportedException('Address Base table is empty')

        self.addresses = self.address_model.objects.filter(
            postcode=self.postcode.with_space)
        if not self.addresses:
            raise self.address_model.DoesNotExist(
                'No addresses found for postcode %s' % (self.postcode))

        self.uprns = self.onsud_model.objects.filter(
            uprn__in=self._get_uprns())

    def _get_uprns(self):
        return [a.uprn for a in self.addresses]

    @property
    def centroid(self):
        return self.addresses.centroid

    def get_code(self, code_type, uprn=None):
        # check the code_type field exists on our model
        self.onsud_model._meta.get_field(code_type)

        if uprn:
            self.addresses.get(uprn=uprn)
            return getattr(self.uprns.get(uprn=uprn), code_type)

        if len(self.uprns) == 0:
            # No records in the ONSUD table were found for the given UPRNs
            # because...reasons
            raise CodesNotFoundException('Found no records in ONSUD for supplied UPRNs')
        if len(self.addresses) != len(self.uprns):
            # For the moment I'm going to do nothing about this, but lets
            # leave this condition here to make that decision explicit
            # TODO: maybe we should actually do....something else??
            pass

        codes = set([getattr(u, code_type) for u in self.uprns])
        if len(codes) == 1:
            # all the uprns supplied are in the same area
            return list(codes)[0]
        else:
            raise MultipleCodesException(
                "Postcode %s covers UPRNs in more than one '%s' area" %\
                (self.postcode, code_type)
            )
