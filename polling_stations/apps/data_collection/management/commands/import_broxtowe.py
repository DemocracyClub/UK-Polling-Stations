from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'E07000172'
    districts_name = 'Broxtowe_Polling_Information'
    stations_name = 'Broxtowe_Polling_Stations.shp'
    elections = [
        'local.nottinghamshire.2017-05-04',
        #'parl.2017-06-08'
    ]

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[5].strip(),
            'name': record[5].strip(),
            'polling_station_id': record[5].strip(),
        }

    def station_record_to_dict(self, record):
        # attempt to lay the address out a bit more nicely
        address = record[2]\
            .strip()\
            .replace(" Nottinghamshire ", "\nNottinghamshire\n")\
            .replace(" Nottinghamshire", "\nNottinghamshire")

        return {
            'internal_council_id': record[4].strip(),
            'postcode': record[3].strip(),
            'address': address,
        }
