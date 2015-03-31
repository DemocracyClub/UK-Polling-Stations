import json

import shapefile

from django.contrib.gis.geos import Point, GEOSGeometry

from data_collection.management.commands import BaseShpImporter
from pollingstations.models import PollingStation, PollingDistrict


class Command(BaseShpImporter):
    srid = 27700

    def import_data(self):
        self.import_polling_districts()
        self.import_polling_stations()

    def import_polling_districts(self):
        sf = shapefile.Reader("{0}/{1}".format(
            self.base_folder_path,
            self.districts_name
            ))
        for district in sf.shapeRecords():
            district_info = self.district_record_to_dict(district.record)
            # import ipdb; ipdb.set_trace()

            geojson = json.dumps(district.shape.__geo_interface__)
            poly = self.clean_poly(GEOSGeometry(geojson, srid=self.srid))

            district_info['area'] = poly
            # import ipdb; ipdb.set_trace()
            self.add_polling_district(district_info)

    def district_record_to_dict(self, record):
        return {
            'council': self.council,
            'name': record[1],
            'internal_council_id': record[2],
        }

    def add_polling_district(self, district_info):
        PollingDistrict.objects.update_or_create(
            council=self.council,
            internal_council_id=district_info['internal_council_id'],
            defaults=district_info,
        )

    def import_polling_stations(self):
        sf = shapefile.Reader("{0}/{1}".format(
            self.base_folder_path,
            self.stations_name
            ))
        for station in sf.shapeRecords():
            station_info = self.station_record_to_dict(station.record)
            station_info['location'] = Point(
                *station.shape.points[0],
                srid=self.srid)
            self.add_polling_station(station_info)

    def station_record_to_dict(self, record):
        return {
            'council': self.council,
            'internal_council_id': record[2],
            'address': record[3].decode('cp1252'),
        }

    def add_polling_station(self, station_info):
        PollingStation.objects.update_or_create(
            council=self.council,
            internal_council_id=station_info['internal_council_id'],
            defaults=station_info,
        )

