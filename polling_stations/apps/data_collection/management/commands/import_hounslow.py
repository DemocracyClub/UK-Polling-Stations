import os
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseHalaroseCsvImporter
from pollingstations.models import PollingStation

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E09000018'
    addresses_name  = 'local.2018-05-03/Version 1/polling_station_export-2018-02-21 (1) Hounslow.csv'
    stations_name   = 'local.2018-05-03/Version 1/polling_station_export-2018-02-21 (1) Hounslow.csv'
    elections       = ['local.2018-05-03']
    csv_encoding    = 'windows-1252'

    def get_station_hash(self, record):
        return "-".join([
            record.pollingstationnumber.strip(),
        ])

    # Hounslow have supplied an additional file with
    # better grid references for the polling stations
    def post_import(self):
        filepath = os.path.join(
            self.base_folder_path,
            'local.2018-05-03/Version 1/2018 Hounslow polling stations - GIS co-ordinates.csv'
        )
        gridrefs = self.get_data('csv', filepath)

        print("Updating grid refs...")
        for record in gridrefs:
            stations = PollingStation.objects.filter(
                council_id=self.council_id,
                internal_council_id=self.get_station_hash(record)
            )
            if len(stations) == 1:
                station = stations[0]
                station.location = Point(
                    float(record.cntr_x),
                    float(record.cntr_y),
                    srid=27700
                )
                self.check_station_point({
                    'location': station.location,
                    'council_id': station.council_id,
                })
                station.save()
            else:
                print("Could not find station id " + self.get_station_hash(record))
        print("...done")
