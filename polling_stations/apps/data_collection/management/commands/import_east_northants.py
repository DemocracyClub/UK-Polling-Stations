from data_collection.morph_importer import BaseMorphApiImporter

class Command(BaseMorphApiImporter):

    srid = 27700
    districts_srid = 27700
    council_id = 'E07000152'
    elections = ['local.northamptonshire.2017-05-04']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-EastNorthamptonshire'
    geom_type = 'gml'
    lookup_table = {}

    def add_to_lookup(self, record):
        """
        This data does not have a code linking the station and district,
        but the station addresses are in the districts output and the
        addresses are consistently formatted across outputs.
        As we process the districts we can build up a lookup of
        station address -> district id.
        Then we can use this later when we process the stations.
        """
        if record['PollingStationAddress'] in self.lookup_table:
            self.lookup_table[record['PollingStationAddress']].append(record['OBJECTID_1'])
        else:
            self.lookup_table[record['PollingStationAddress']] = [record['OBJECTID_1']]

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
            '<wfs:FeatureCollection xmlns:elections_elections="http://giscoresrv.east-northamptonshire.gov.uk:6080/arcgis/services/elections/elections/MapServer/WFSServer" xmlns:gml="http://www.opengis.net/gml" xmlns:wfs="http://www.opengis.net/wfs" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://giscoresrv.east-northamptonshire.gov.uk:6080/arcgis/services/elections/elections/MapServer/WFSServer https://mapsenc.east-northamptonshire.gov.uk/arcgis/services/elections/elections/MapServer/WFSServer?request=DescribeFeatureType%26version=1.1.0%26typename=Polling_Districts http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd http://www.opengis.net/gml http://schemas.opengis.net/gml/3.1.1/base/gml.xsd">',
            '<wfs:FeatureCollection xmlns:elections_elections="http://giscoresrv.east-northamptonshire.gov.uk:6080/arcgis/services/elections/elections/MapServer/WFSServer" xmlns:gml="http://www.opengis.net/gml" xmlns:wfs="http://www.opengis.net/wfs" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd http://www.opengis.net/gml http://schemas.opengis.net/gml/3.1.1/base/gml.xsd">'
        )
        return record

    def district_record_to_dict(self, record):
        self.add_to_lookup(record)
        record = self.replace_schema(record)
        
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))
        return {
            'internal_council_id': record['OBJECTID_1'],
            'name'               : record['Code_District'],
            'area'               : poly,
        }

    def station_record_to_dict(self, record):
        location = self.extract_geometry(record, self.geom_type, self.get_srid('stations'))

        # match up the station addresses with the lookup we built earlier
        if record['Address'] in self.lookup_table:
            codes = self.lookup_table[record['Address']]
        else:
            # There are 3 stations which don't serve any district
            return None

        stations = []
        for code in codes:
            stations.append({
                'internal_council_id': code,
                'postcode':            '',
                'address':             "%s, %s" % (record['Name'], record['Address']),
                'location':            location,
                'polling_district_id': code,
            })
        return stations
