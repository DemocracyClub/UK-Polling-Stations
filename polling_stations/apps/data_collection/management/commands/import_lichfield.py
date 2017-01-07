from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

"""
Lichfield publish their data on data.gov.uk as zipped shp files

I've uploaded the data to Amazon S3 for import purposes

Additionally there's a hashes only scraper at
https://morph.io/wdiv-scrapers/DC-PollingStations-Lichfield
polling the URLs to look for changes.
"""

class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'E07000194'
    districts_name = 'local.staffordshire.2017-05-04/Lichfield District Council Polling Districts Shapefile/Lichfield District Council Polling Districts'
    stations_name = 'local.staffordshire.2017-05-04/LDC_Polling_Stations_Shapefile/Lichfield_District_Council_Polling_Station_Locations.shp'
    elections = ['local.staffordshire.2017-05-04']

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': str(record[3]).strip(),
            'name': str(record[3]).strip(),
            'polling_station_id': str(record[3]).strip(),
        }

    def station_record_to_dict(self, record):
        address = "\n".join([
            str(record[1]).strip(),
            str(record[4]).strip(),
        ])
        postcode = str(record[5]).strip()
        codes = [record[9].strip(), record[10].strip(), record[11].strip()]

        stations = []
        for code in codes:
            if code != b'':
                stations.append({
                    'internal_council_id': str(code),
                    'postcode'           : postcode,
                    'address'            : address,
                })
        return stations
