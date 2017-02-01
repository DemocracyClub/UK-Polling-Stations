from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseCsvStationsShpDistrictsImporter

class Command(BaseCsvStationsShpDistrictsImporter):
    srid = 27700
    council_id = 'E07000221'
    districts_name = 'Polling_Districts'
    stations_name = 'Copy of Polling Station Details - Revised.csv'
    elections = ['local.warwickshire.2017-05-04']

    """
    File supplied contains 154 districts and 148 stations.
    Orphan districts are JD1, DK2, EB2, DJ2, DH2, DU1.
    Joe queried with council. Fedback was:

    The polling districts you list were created in 2015 to accommodate changes to our District ward boundaries.
    However in 2015 what had not changed were the County division boundaries so temporary polling districts were
    created to allow for any County by-election occurring before new County divisions were in place. In creating a
    register to publish for 2017 the temporary polling districts became superfluous so were therefore absorbed elsewhere as follows:
    JD1 joined JD
    DK2 joined DK1
    EB2 joined EB (not EB1)
    DJ2 joined DJ1
    DH2 joined DH1
    DU1 joined DU

    This mapping allows us to assign the correct stations to the orphan districts
    """
    districts_map = {
        'JD': 'JD1',
        'DK1': 'DK2',
        'EB': 'EB2',
        'DJ1': 'DJ2',
        'DH1': 'DH2',
        'DU': 'DU1',
    }

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': str(record[0]).strip(),
            'name': "%s - %s" % (str(record[3]).strip(), str(record[0]).strip()),
        }

    def station_record_to_dict(self, record):
        location = Point(float(record.e), float(record.n), srid=self.srid)
        stations = []
        district_id = record.district_s_.strip()
        station = {
            'internal_council_id': district_id,
            'address' : "\n".join(
                [record.name.strip(), record.address.strip()]),
            'postcode': '',
            'polling_district_id': district_id,
            'location': location,
        }
        stations.append(station)

        # apply manual corrections
        if district_id in self.districts_map:
            station2 = station.copy()
            station2['internal_council_id'] = self.districts_map[district_id]
            station2['polling_district_id'] = self.districts_map[district_id]
            stations.append(station2)

        return stations
