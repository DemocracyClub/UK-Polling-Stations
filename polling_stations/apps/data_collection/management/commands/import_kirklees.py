from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter
from uk_geo_utils.geocoders import AddressBaseGeocoder, AddressBaseException


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E08000034'
    addresses_name = 'local.2018-05-03/Version 3/Democracy_Club__03May2018.tsv'
    stations_name = 'local.2018-05-03/Version 3/Democracy_Club__03May2018.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '83099017':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'BD19 5EY'
            return rec

        if uprn == '200003798939':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'HD7 5TU'
            return rec

        if uprn == '83242159':
            return None

        if uprn == '83246005':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'HD2 1HA'
            return rec

        return super().address_record_to_dict(record)

    def get_station_point(self, record):
        location = None

        if (hasattr(record, self.easting_field) and\
            hasattr(record, self.northing_field) and\
            getattr(record, self.easting_field) != '0' and\
            getattr(record, self.easting_field) != '' and\
            getattr(record, self.northing_field) != '0' and\
            getattr(record, self.northing_field) != ''):

            # if we've got points, use them
            location = Point(
                float(getattr(record, self.easting_field)),
                float(getattr(record, self.northing_field)),
                srid=27700)
        elif self.station_uprn_field and getattr(record, self.station_uprn_field).strip():
            # if we have a UPRN, try that
            try:
                uprn = getattr(record, self.station_uprn_field)
                uprn = uprn.lstrip('0')
                g = AddressBaseGeocoder(self.get_station_postcode(record))
                location = g.get_point(getattr(record, self.station_uprn_field))
            except (ObjectDoesNotExist, AddressBaseException) as e:
                # otherwise, don't set a point
                location = None
        else:
            # otherwise, don't set a point
            location = None

        return location
