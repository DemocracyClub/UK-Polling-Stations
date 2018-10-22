import abc

from django.core.exceptions import ObjectDoesNotExist

from uk_geo_utils.helpers import Postcode
from uk_geo_utils.geocoders import (
    AddressBaseGeocoder,
    OnspdGeocoder,
    AddressBaseException,
    MultipleCodesException
)

from pollingstations.models import Council


class PostcodeError(Exception):
    pass

class MultipleCouncilsException(MultipleCodesException):
    pass


class BaseGeocoder(metaclass=abc.ABCMeta):

    def __init__(self, postcode):
        self.postcode = self.format_postcode(postcode)

    def format_postcode(self, postcode):
        return Postcode(postcode).without_space

    @abc.abstractmethod
    def geocode_point_only(self):
        pass

    @abc.abstractmethod
    def geocode(self):
        pass


class OnspdGeocoderAdapter(BaseGeocoder):

    def geocode(self):
        geocoder = OnspdGeocoder(self.postcode)
        centre = geocoder.centroid
        if not centre:
            raise PostcodeError("No location information")

        local_auth = geocoder.get_code('lad')
        error_values = [
            'L99999999', # Channel Islands
            'M99999999', # Isle of Man
            '' # Terminated Postcode or other
        ]
        if not local_auth or local_auth in error_values:
            raise PostcodeError("No location information")

        return geocoder

    def geocode_point_only(self):
        geocoder = OnspdGeocoder(self.postcode)
        centre = geocoder.centroid
        if not centre:
            raise PostcodeError("No location information")
        return geocoder


class AddressBaseGeocoderAdapter(BaseGeocoder):

    def geocode(self):
        geocoder = AddressBaseGeocoder(self.postcode)
        centre = geocoder.centroid

        try:
            lad = geocoder.get_code('lad')
        except MultipleCodesException as e:
            # re-raise as a more specific MultipleCouncilsException
            # because that is what the calling code expects to handle
            raise MultipleCouncilsException(str(e))

        return geocoder

    def geocode_point_only(self):
        return AddressBaseGeocoder(self.postcode)


def geocode_point_only(postcode):
    geocoders = (AddressBaseGeocoderAdapter(postcode), OnspdGeocoderAdapter(postcode))
    for geocoder in geocoders:
        try:
            return geocoder.geocode_point_only()
        except ObjectDoesNotExist:
            # we couldn't find this postcode in AddressBase
            # this might be because
            # - The postcode isn't in AddressBase
            # - The postcode is in Northern Ireland
            # - AddressBase hasn;t been imported
            # fall back to the next source
            continue
        except PostcodeError:
            # we were unable to geocode this postcode using ONSPD
            # re-raise the exception.
            # Note: in future we may want to fall back to yet another source
            raise

    # All of our attempts to geocode this failed. Raise a generic exception
    raise PostcodeError('Could not geocode from any source')


def geocode(postcode):
    geocoders = (AddressBaseGeocoderAdapter(postcode), OnspdGeocoderAdapter(postcode))
    for geocoder in geocoders:
        try:
            return geocoder.geocode()
        except ObjectDoesNotExist:
            # we couldn't find this postcode in AddressBase
            # this might be because
            # - The postcode isn't in AddressBase
            # - The postcode is in Northern Ireland
            # - AddressBase hasn;t been imported
            # fall back to the next source
            continue
        except MultipleCouncilsException:
            # this postcode contains uprns in multiple local authorities
            # re-raise the exception.
            raise
        except AddressBaseException:
            # we did find this postcode in AddressBase, but there were no
            # corresponding codes in ONSUD: fall back to the next source
            continue
        except PostcodeError:
            # we were unable to geocode this postcode using ONSPD
            # re-raise the exception.
            # Note: in future we may want to fall back to yet another source
            raise

    # All of our attempts to geocode this failed. Raise a generic exception
    raise PostcodeError('Could not geocode from any source')


def get_council(geocode_result):
    try:
        return Council.objects.defer("area").get(
            council_id=geocode_result.get_code('lad'))
    except Council.DoesNotExist:
        return Council.objects.defer("area").get(
            area__covers=geocode_result.centroid)
