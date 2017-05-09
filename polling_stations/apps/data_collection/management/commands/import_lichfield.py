from data_collection.management.commands import BaseApiShpZipStationsShpZipDistrictsImporter

class Command(BaseApiShpZipStationsShpZipDistrictsImporter):
    srid = 27700
    districts_srid = 27700
    council_id = 'E07000194'
    districts_url = 'https://www.lichfielddc.gov.uk/Inspire-data-sets/Lichfield%20District%20Council%20Polling%20Districts/Lichfield%20District%20Council%20Polling%20Districts%20Shapefile.zip'
    stations_url = 'https://www.lichfielddc.gov.uk/Inspire-data-sets/Lichfield%20District%20Council%20Polling%20Stations/LDC_Polling_Stations_Shapefile.zip'
    elections = [
        'local.staffordshire.2017-05-04',
        'parl.2017-06-08'
    ]

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': str(record[4]).strip(),
            'name': str(record[4]).strip(),
            'polling_station_id': str(record[4]).strip(),
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
