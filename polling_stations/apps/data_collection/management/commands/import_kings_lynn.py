"""
Queried several data quality problems and received following notes:

PM2 vote at the King’s Centre, Wellesley Street, King’s Lynn
PR6 vote at Brancaster Staithe Village Hall only
RP6 go to Amy Robsart Village Hall
RX6 go to West Newton Village Hall
SC1 vote at Harpley Village Hall
SC7 and RX1 don’t exist
PM1 vote with PM2 at the King’s Centre

This script contains various manual fixes for these issues
"""

from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'E07000146'
    districts_name = 'parl.2017-06-08/Version 1/BCKLWN_polling_districts/Polling_districts.shp'
    stations_name = 'parl.2017-06-08/Version 2/Polling_Stations_June17.shp'
    elections = ['parl.2017-06-08']
    seen_districts = set()

    def district_record_to_dict(self, record):
        code = str(record[2]).strip()

        # Code PM2 appears twice
        # One of them is supposed to be PM1
        # We don't know which one, but they both vote at the same station
        # So just assign one them code PM1.. it doesn;t change anything
        if code == 'PM2' and code in self.seen_districts:
            code = 'PM1'
        self.seen_districts.add(code)

        return {
            'internal_council_id': code,
            'name': str(record[1]).strip(),
        }

    def parse_string(self, text):
        try:
            return text.strip().decode('utf-8')
        except AttributeError:
            return text.strip()

    def get_address(self, record):
        address_parts = [self.parse_string(x) for x in record[2:7] if x != 'NULL']
        address = "\n".join(address_parts)
        while "\n\n" in address:
            address = address.replace("\n\n", "\n").strip()
        return address

    def station_record_to_dict(self, record):
        stations = []

        codes = str(record[11]).strip()

        if codes == 'NOT USED':
            return None
        codes = codes.split(' ')

        # manual fixes for various dodgy codes
        if str(record[2]).strip() == 'Amy Robsart Village Hall':
            codes = ['RP6', 'RP7']
        if str(record[2]).strip() == 'West Newton Village Hall':
            codes.append('RX6')
        if str(record[2]).strip() == 'Harpley Village Hall':
            codes.append('SC1')

        for code in codes:
            stations.append({
                'internal_council_id': code,
                'postcode': str(record[8]).strip(),
                'address': self.get_address(record),
                'polling_district_id': code,
            })

        return stations
