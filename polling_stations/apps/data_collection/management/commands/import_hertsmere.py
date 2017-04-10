from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    council_id = 'E07000098'
    srid = 27700
    districts_srid = 27700
    districts_name = 'PollingDistricts'
    stations_name = 'PollingStations.shp'
    elections = ['local.hertfordshire.2017-05-04']

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': str(record[0]).strip(),
            'name': str(record[1]).strip(),
            'polling_station_id': str(record[0]).strip(),
        }

    def format_address(self, record):
        address_parts = [str(record[x]).strip() for x in range(3, 7)]
        for i, part in enumerate(address_parts):
            if part[:2] == "b'":
                address_parts[i] = ''
        for i, part in enumerate(address_parts):
            if len(part) <= 3 and len(part) > 0:
                address_parts[i+1] = part + ' ' + address_parts[i+1]
                address_parts[i] = ''
                break
        address = "\n".join(address_parts)
        while "\n\n" in address:
            address = address.replace("\n\n", "\n")
        return address.strip()

    def station_record_to_dict(self, record):
        postcode = str(record[8]).strip('\'b').strip()
        return {
            'internal_council_id': str(record[1]).strip(),
            'address' : self.format_address(record),
            'postcode': postcode,
        }
