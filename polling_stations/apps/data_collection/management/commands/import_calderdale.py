"""
Import Calderdale
"""
import json
import shapefile
from django.contrib.gis.geos import GEOSGeometry, Point
from data_collection.management.commands import BaseShpImporter

class Command(BaseShpImporter):
    """
    Imports the Polling Station data from Calderdale
    """
    council_id       = 'E08000033'
    districts_name   = 'polling_districts'
    stations_name    = 'Polling Stations.csv'
    elections        = [
        'pcc.2016-05-05',
        'ref.2016-06-23'
    ]
    missing_stations = []

    def import_polling_districts(self):
        sf = shapefile.Reader("{0}/{1}".format(
            self.base_folder_path,
            self.districts_name
            ))
        for district in sf.shapeRecords():
            district_info = self.district_record_to_dict(district.record)
            if 'council' not in district_info:
                district_info['council'] = self.council

            geojson = json.dumps(district.shape.__geo_interface__)
            poly = self.clean_poly(GEOSGeometry(geojson, srid=self.get_srid('districts')))

            """
            File contains 2 districts with the code DC. One of them covers a distinct
            area not covered by another district. The other exactly contains districts
            DD and DE. I've assumed that the one covering a distinct area is 'correct'
            (i.e: A property may not be in 2 districts simultaneously).
            Discard the other district DC.
            """
            if district.record[1] == 'DC' and poly.length == 16675.9905799729:
                pass
            else:
                district_info['area'] = poly
                self.add_polling_district(district_info)

    def district_record_to_dict(self, record):

        """
        Districts BB and BC don't appear in the stations file
        but the station addresses are embedded in the districts
        file. Save them for later.
        """
        if record[1] == 'BB' or record[1] == 'BC':
            self.missing_stations.append(record)

        return {
            'internal_council_id': record[1],
            'name'               : "%s - %s" % (record[0], record[1]),
            'polling_station_id' : record[1]
        }

    def split_address(self, in_address):
        address_parts = in_address.replace('.', '').split(", ")

        if (len(address_parts[-1]) == 7 or len(address_parts[-1]) == 8) and address_parts[-1] != 'Halifax':
            out_address = "\n".join(address_parts[:-1])
            postcode = address_parts[-1]
        else:
            out_address = "\n".join(address_parts)
            postcode = ''

        return {
            'address'  : out_address,
            'postcode' : postcode
        }

    def station_record_to_dict(self, record):

        # discard the rows with no district id/address
        if not record.polling_district:
            return None

        location = Point(float(record.easting), float(record.northing), srid=self.get_srid())

        address_parts = self.split_address(record.address)

        return {
            'internal_council_id': record.polling_district,
            'postcode'           : address_parts['postcode'],
            'address'            : address_parts['address'],
            'location'           : location
        }

    def post_import(self):
        # iterate self.missing_stations + insert
        # points are missing and we have no postcodes to geocode
        for record in self.missing_stations:
            address_parts = self.split_address(record[2])
            self.add_polling_station({
                'internal_council_id': record[1],
                'postcode'           : address_parts['postcode'],
                'address'            : address_parts['address'],
                'location'           : None
            })
