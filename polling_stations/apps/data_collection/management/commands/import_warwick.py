from data_collection.management.commands import BaseShpStationsShpDistrictsImporter

class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'E07000222'
    districts_name = 'POLLD4 (1)'
    stations_name = 'POLLINST.shp'
    elections = ['local.warwickshire.2017-05-04']

    def get_station_hash(self, record):
        return record.record[0]

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': str(record[1]).strip().upper(),
            'name': "%s - %s" % (
                str(record[1]).strip().upper(),
                str(record[0]).strip()
            ),
        }

    def station_record_to_dict(self, record):

        # WMH1 has 2 polling stations in the same location: merge them
        if record[0] == 'WMH1':
            return {
                'internal_council_id': str(record[0]).strip().upper(),
                'address'            : "\n".join([
                    'Temporary Building (Stations A & B), Myton Fields Car Park',
                    str(record[2]).strip(),
                    str(record[3]).strip(),
                ]),
                'polling_district_id': str(record[0]).strip().upper(),
            }

        return {
            'internal_council_id': str(record[0]).strip().upper(),
            'address'            : "\n".join([
                str(record[1]).strip(),
                str(record[2]).strip(),
                str(record[3]).strip(),
            ]),
            'polling_district_id': str(record[0]).strip().upper(),
        }
