from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'E07000078'
    districts_name = 'fixed_districts/Polling_districts'
    stations_name = 'Cheltenham_Polling_stations.shp'
    elections = [
        'parl.2017-06-08'
    ]

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[2].strip(),
            'name': "%s - %s" % (record[2], record[1]),
            'polling_station_id': record[2].strip()
        }

    def station_record_to_dict(self, record):

        if '/' in record[2]:
            codes = record[2].split('/')
        elif ',' in record[2]:
            codes = record[2].split(',')
        else:
            codes = [record[2]]

        stations = []
        for code in codes:

            if code == 'LA':
                address = "\n".join([
                    'Pittville Pump Room',
                    str(record[0]).strip()
                ])
            else:
                address = "\n".join([
                    str(record[1]).strip(),
                    str(record[0]).strip()
                ])

            station = {
                'internal_council_id': code.strip(),
                'postcode'           : '',
                'address'            : address,
            }

            if code.strip() == 'MA1' or code.strip() == 'MA2':
                station['internal_council_id'] = 'MA'
                return station
            elif code.strip() == 'DA1' or code.strip() == 'DA2':
                station['internal_council_id'] = 'DA'
                return station
            else:
                stations.append(station)

        return stations
