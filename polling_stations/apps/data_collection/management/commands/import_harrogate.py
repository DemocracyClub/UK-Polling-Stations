from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'E07000165'
    districts_name = '4 April 2017/POLLDISTOPEN'
    stations_name = '4 April 2017/POLLSTAOPEN.shp'
    elections = ['local.north-yorkshire.2017-05-04']

    def district_record_to_dict(self, record):
        code = str(record[0]).strip()
        return {
            'internal_council_id': code,
            'name': code,
            'polling_station_id': code,
        }

    def format_address(self, record):
        address_parts = [
            str(record[4]).strip('\'b').strip(),
            str(record[5]).strip('\'b').strip(),
            str(record[6]).strip('\'b').strip(),
            str(record[7]).strip('\'b').strip(),
            str(record[8]).strip('\'b').strip(),
        ]
        if str(record[3]).strip('\'b').strip():
            address_parts.insert(0, str(record[3]).strip('\'b').strip())
        address = "\n".join(address_parts)
        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()
        return address

    def station_record_to_dict(self, record):
        return {
            'internal_council_id': str(record[0]).strip(),
            'postcode': '',
            'address': self.format_address(record),
            'polling_district_id': str(record[0]).strip(),
        }
