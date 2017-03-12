from data_collection.management.commands import BaseXpressCsvImporter

class Command(BaseXpressCsvImporter):
    council_id = 'E07000011'
    addresses_name = 'Hunts_Democracy_Club__04May2017.tsv'
    stations_name = 'Hunts_Democracy_Club__04May2017.tsv'
    elections = ['mayor.cambridgeshire-and-peterborough.2017-05-04']
    csv_delimiter = '\t'
    station_postcode_field = 'polling_place_postcode'
    station_address_fields = [
        'polling_place_name',
        'polling_place_address_1',
        'polling_place_address_2',
        'polling_place_address_3',
        'polling_place_address_4',
    ]
    station_id_field = 'polling_place_id'
    easting_field = 'polling_place_easting'
    northing_field = 'polling_place_northing'


    def address_record_to_dict(self, record):
        address = ", ".join([
            record.addressline1,
            record.addressline2,
            record.addressline3,
            record.addressline4,
            record.addressline5,
        ])
        while ", , " in address:
            address = address.replace(", , ", ", ")
        if address[-2:] == ', ':
            address = address[:-2]

        return {
            'address'           : address.strip(),
            'postcode'          : record.addressline6.strip(),
            'polling_station_id': getattr(record, self.station_id_field).strip()
        }
