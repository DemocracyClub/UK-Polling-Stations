from data_collection.management.commands import BaseCsvStationsShpDistrictsImporter

class Command(BaseCsvStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'E07000113'
    districts_name = 'shp/Swale Polling Districts'
    stations_name = 'Swale 21 Feb 2017 Polling scheme station numbers.csv'
    elections = [
        'local.kent.2017-05-04',
        'parl.2017-06-08'
    ]

    def district_record_to_dict(self, record):
        code = str(record[0]).strip()
        return {
            'internal_council_id': code,
            'name': str(record[1]).strip(),
        }

    def station_record_to_dict(self, record):
        codes = record.pd.split(" and ")
        stations = []
        for code in codes:
            stations.append({
                'internal_council_id': code,
                'postcode': '',
                'address': record.premises,
                'polling_district_id': code,
                'location': None,
            })
        return stations
