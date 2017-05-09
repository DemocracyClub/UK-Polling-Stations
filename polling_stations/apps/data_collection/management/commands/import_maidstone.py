from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'E07000110'
    districts_name = 'shp/maidstone_polling_districts'
    stations_name = 'shp/maidstone_polling_stations.shp'
    elections = [
        'local.kent.2017-05-04',
        'parl.2017-06-08'
    ]

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[0].strip(),
            'name': record[1].strip(),
            'polling_station_id': record[0].strip(),
        }

    def station_record_to_dict(self, record):
        address_parts = record[3].strip().split(", ")
        address_parts.insert(0, record[2].strip())
        address = "\n".join(address_parts)
        return {
            'internal_council_id': record[0].strip(),
            'postcode': record[18].strip(),
            'address': address,
        }
