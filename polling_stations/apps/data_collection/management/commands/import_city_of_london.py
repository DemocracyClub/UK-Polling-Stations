"""
Imports City of London
"""
from django.contrib.gis.geos import GEOSGeometry
from data_collection.management.commands import BaseApiKmlKmlImporter

class Command(BaseApiKmlKmlImporter):
    """
    Imports the Polling Station data from City of London Corporation
    """
    srid             = 27700
    districts_srid   = 27700
    council_id       = 'E09000001'
    districts_url    = 'http://www.mapping2.cityoflondon.gov.uk/arcgis/services/INSPIRE/MapServer/WFSServer?request=GetFeature&version=1.1.0&service=wfs&typeNames=INSPIRE:UK_Parliamentary_General_Election_Polling_Districts'
    stations_url     = 'http://www.mapping2.cityoflondon.gov.uk/arcgis/services/INSPIRE/MapServer/WFSServer?request=GetFeature&version=1.1.0&service=wfs&typeNames=INSPIRE:UK_Parliamentary_General_Election_Polling_Places'
    """
    note:
    These aren't actually KML - they're QML (hence use of SRID 27700)
    but gdal.DataSource will just deal with them for us :)
    """

    def district_record_to_dict(self, record):
        geojson = record.geom.geojson
        poly = self.clean_poly(GEOSGeometry(geojson, srid=self.get_srid('districts')))

        return {
            'internal_council_id': record['OBJECTID'],
            'name'               : record['POLLING_DISTRICT'],
            'area'               : poly
        }

    def station_record_to_dict(self, record):
        geojson = record.geom.geojson
        location = GEOSGeometry(geojson, srid=self.get_srid())


        # format address and postcode
        address = str(record['Address'])
        address_parts = address.split(', ')
        postcode = address_parts[-1]

        if postcode[:1] == 'E':
            del(address_parts[-1])
        else:
            postcode = address_parts[-1][-8:]
            address_parts[-1] = address_parts[-1][:-9]

        address = "\n".join(address_parts)


        return {
            'internal_council_id': record['OBJECTID'],
            'postcode':            postcode,
            'address':             address,
            'location':            location
        }
