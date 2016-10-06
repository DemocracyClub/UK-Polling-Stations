"""
Imports Pembrokeshire
"""
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode_point_only, PostcodeError

class Command(BaseCsvStationsCsvAddressesImporter):
    """
    Imports the Polling Station data from Pembrokeshire
    """
    council_id      = 'W06000009'
    addresses_name  = 'GAZETTEER_DATA.CSV'
    stations_name   = 'ERCOVER.DTA'
    elections       = [
        'pcc.2016-05-05',
        'naw.c.2016-05-05',
        'naw.r.2016-05-05',
        'ref.2016-06-23'
    ]

    def station_record_to_dict(self, record):

        # Don't import the Carmarthenshire polling stations
        # We don't have the address data to go with them :(
        if record.local_auth == 'W06000010':
            return None

        # format address
        address_parts = []
        if record.bldg_name:
            address_parts.append(record.bldg_name)
        if record.bldg_add1:
            address_parts.append(record.bldg_add1)
        if record.bldg_add2:
            address_parts.append(record.bldg_add2)
        if record.bldg_add3:
            address_parts.append(record.bldg_add3)
        if record.bldg_add4:
            address_parts.append(record.bldg_add4)
        if record.bldg_add5:
            address_parts.append(record.bldg_add5)
        address = "\n".join(address_parts)

        # convert postcode to upper case
        postcode = record.bldg_pcode.upper()

        if record.kml_lng and record.kml_lat:
            location = Point(float(record.kml_lng), float(record.kml_lat), srid=4326)
        else:
            # there is one station we don't have a point for - geocode it
            try:
                gridref = geocode_point_only(postcode)
                location = Point(gridref['wgs84_lon'], gridref['wgs84_lat'], srid=4326)
            except PostcodeError:
                location = None

        return {
            'internal_council_id': record.district,
            'postcode'           : postcode,
            'address'            : address,
            'location'           : location
        }

    def address_record_to_dict(self, record):

        # format address
        address_parts = []
        if record.address1:
            address_parts.append(record.address1)
        if record.address2:
            address_parts.append(record.address2)
        if record.address3:
            address_parts.append(record.address3)
        if record.address4:
            address_parts.append(record.address4)
        if record.address5:
            address_parts.append(record.address5)
        if record.address6:
            address_parts.append(record.address6)
        address = "\n".join(address_parts[:-1])

        return {
            'address'           : address,
            'postcode'          : record.postcode,
            'polling_station_id': record.district_code
        }
