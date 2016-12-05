from data_collection.morph_importer import BaseMorphApiImporter

class Command(BaseMorphApiImporter):

    srid = 27700
    districts_srid = 27700
    council_id = 'E09000001'
    elections = [
        'gla.c.2016-05-05',
        'gla.a.2016-05-05',
        'mayor.london.2016-05-05',
        'ref.2016-06-23',
    ]
    scraper_name = 'wdiv-scrapers/DC-PollingStations-CityOfLondon'
    geom_type = 'gml'


    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))

        return {
            'internal_council_id': record['OBJECTID'],
            'name'               : record['POLLING_DISTRICT'],
            'area'               : poly
        }


    def station_record_to_dict(self, record):
        location = self.extract_geometry(record, self.geom_type, self.get_srid('stations'))


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
