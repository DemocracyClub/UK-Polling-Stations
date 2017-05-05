from data_collection.morph_importer import BaseMorphApiImporter

class Command(BaseMorphApiImporter):

    srid = 27700
    districts_srid = 27700
    council_id = 'E07000156'
    elections = ['parl.2017-06-08']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Wellingborough'
    geom_type = 'gml'

    def replace_schema(self, record):
        """
        This data is represented as a MultiSurface element,
        which is not supported. Trying to parse it will throw
        django.contrib.gis.gdal.error.GDALException: Invalid OGR Integer Type: 12

        However, this data doesn't actually contain any Z co-ordinates
        (it is just polygons wrapped in a MultiSurface container) so we can
        'trick' django into just parsing the polygon data by removing the
        custom schema url and forcing it to be parsed using a generic GML/WFS
        schema. This means it will pass over the elements it doesn't understand.

        This is *definitely* not the correct way to do this
        but it gets the job done
        """
        record['geometry'] = record['geometry'].replace(
            '<wfs:FeatureCollection xmlns:electoral_electoral_wfs="http://bcw-giscore.wellingborough.gov.uk:6080/arcgis/services/electoral/electoral_wfs/MapServer/WFSServer" xmlns:gml="http://www.opengis.net/gml" xmlns:wfs="http://www.opengis.net/wfs" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://bcw-giscore.wellingborough.gov.uk:6080/arcgis/services/electoral/electoral_wfs/MapServer/WFSServer http://mapsbcw.wellingborough.gov.uk/arcgis/services/electoral/electoral_wfs/MapServer/WFSServer?request=DescribeFeatureType%26version=1.1.0%26typename=Polling_Districts http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd http://www.opengis.net/gml http://schemas.opengis.net/gml/3.1.1/base/gml.xsd">',
            '<wfs:FeatureCollection xmlns:electoral_electoral_wfs="http://bcw-giscore.wellingborough.gov.uk:6080/arcgis/services/electoral/electoral_wfs/MapServer/WFSServer" xmlns:gml="http://www.opengis.net/gml" xmlns:wfs="http://www.opengis.net/wfs" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd http://www.opengis.net/gml http://schemas.opengis.net/gml/3.1.1/base/gml.xsd">'
        )
        return record

    def district_record_to_dict(self, record):
        record = self.replace_schema(record)
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))

        return {
            'internal_council_id': record['POLLING_DISTRICT_CODE'],
            'name'               : record['POLLING_DISTRICT_NAME'],
            'area'               : poly,
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(record, self.geom_type, self.get_srid('stations'))

        return {
            'internal_council_id': record['DISTRICTS'],
            'postcode':            '',
            'address':             record['ADDRESS'],
            'location':            location,
            'polling_district_id': record['DISTRICTS'],
        }
