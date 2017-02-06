from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseCsvStationsCsvAddressesImporter
from data_finder.helpers import geocode_point_only, PostcodeError

class Command(BaseCsvStationsCsvAddressesImporter):
    council_id      = 'E07000120'
    addresses_name  = 'rev02-2017/Hyndburn_polling_station_export-2017-02-03 (1).csv'
    stations_name   = 'rev02-2017/Hyndburn_polling_station_export-2017-02-03 (1).csv'
    elections       = ['local.lancashire.2017-05-04']

    def get_station_hash(self, record):
        return "-".join([
            record.pollingstationnumber,
        ])

    def station_record_to_dict(self, record):

        address = "\n".join([
            record.pollingstationname,
            record.pollingstationnumber + ' ' + record.pollingstationaddress_1,
            record.pollingstationaddress_2,
            record.pollingstationaddress_3,
            record.pollingstationaddress_4,
            record.pollingstationaddress_5,
        ])

        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()

        postcode = record.pollingstationpostcode

        location = None
        if postcode:
            try:
                location_data = geocode_point_only(postcode)
                location = Point(
                    location_data['wgs84_lon'],
                    location_data['wgs84_lat'],
                    srid=4326)
            except PostcodeError:
                location = None

        return {
            'internal_council_id': record.pollingstationnumber,
            'postcode'           : postcode,
            'address'            : address,
            'location'           : location,
        }


    def address_record_to_dict(self, record):

        def replace_na(text):
            if text.strip() == 'n/a':
                return ''
            return text.strip()

        if record.streetname.strip() == 'Other Electors':
            return None
        if record.housepostcode.strip() == '':
            return None


        address_line_1 = replace_na(record.housename) + ' ' + replace_na(record.housenumber)
        address_line_1 = address_line_1.strip()
        street_address = replace_na(record.streetnumber) + ' ' + replace_na(record.streetname)
        street_address = street_address.strip()
        address_line_1 = address_line_1 + ' ' + street_address

        address = "\n".join([
            address_line_1.strip(),
            replace_na(record.locality),
            replace_na(record.town),
            replace_na(record.adminarea),
        ])

        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()


        return {
            'address'           : address,
            'postcode'          : record.housepostcode.strip(),
            'polling_station_id': record.pollingstationnumber,
        }
