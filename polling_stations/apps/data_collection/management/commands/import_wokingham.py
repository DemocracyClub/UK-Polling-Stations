"""
Import Wokingham Polling stations
"""

from data_collection.management.commands import (
    BaseCsvStationsShpDistrictsImporter,
    import_polling_station_shapefiles
)

class Command(BaseCsvStationsShpDistrictsImporter):
    """
    Imports the Polling Station data from Wokingham Council
    """
    council_id     = 'E06000041'
    districts_name = ''
    stations_name  = 'POLLING_STATIONS_font_point.shp'
    elections      = ['parl.2015-05-07']

    def import_polling_districts(self):
        # Because we don't have them :(
        return 

    def district_record_to_dict(self, record):
        # return {
        #     'council': self.council,
        #     'internal_council_id': record[-1],
        #     'name': record[0],
        # }
        return

    def station_record_to_dict(self, record):
        return {
            'internal_council_id': " ".join(record),
            'postcode'           : '(No postcode supplied)',
            'address'            : "\n".join(record[:-1]),
        }
    
    def import_polling_stations(self):
        import_polling_station_shapefiles(self)
