from data_collection.github_importer import BaseGitHubImporter

class Command(BaseGitHubImporter):

    srid = 4326
    districts_srid  = 4326
    council_id = 'E06000023'
    elections = ['parl.2017-06-08']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Bristol'
    geom_type = 'geojson'

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))
        return {
            'internal_council_id': record['POLLING_DIST_ID'].strip(),
            'name': record['POLLING_DIST_NAME'].strip(),
            'area': poly,
            'polling_station_id': record['POLLING_DIST_ID'].strip(),
        }

    def extract_codes(self, text):
        """
        Bristol's data does tell us about stations that serve multiple stations
        but not in a very nice way e.g:

        CEND and CENB
        SGWD & SGWB
        Used by CLIB and CLIA
        Used by REDC amd REDG
        Used by BEDA & BEDC

        Attempt to make sense of this
        """
        stations = text
        stations = stations.replace('Used by', '')
        stations = stations.replace('Used bu', '')
        stations = stations.replace('Used for', '')
        codes = []
        if 'and' in stations:
            codes = stations.split('and')
        elif 'amd' in stations:
            codes = stations.split('amd')
        elif '&' in stations:
            codes = stations.split('&')
        else:
            raise ValueError("Could not parse 'DUAL_STN' field: %s" % text)

        codes = [code.strip() for code in codes]

        if len(codes) < 2:
            raise ValueError("Could not parse 'DUAL_STN' field: %s" % text)

        return codes

    def station_record_to_dict(self, record):
        location = self.extract_geometry(record, self.geom_type, self.get_srid('stations'))

        address_parts = [record['PAO'].strip(), record['STREET'].strip()]
        if record['LOCALITY']:
            address_parts.append(record['LOCALITY'].strip())
        address = "\n".join(address_parts)

        postcode = ''
        if record['POSTCODE']:
            postcode = record['POSTCODE'].strip()

        if record['DUAL_STN']:
            codes = self.extract_codes(record['DUAL_STN'])
        else:
            codes = [record['POLLING_DISTRICT'].strip()]

        stations = []
        for code in codes:
            stations.append({
                'internal_council_id': code,
                'postcode': postcode,
                'address': address,
                'location': location,
            })
        return stations
