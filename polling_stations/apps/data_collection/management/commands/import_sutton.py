import os
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseHalaroseCsvImporter
from pollingstations.models import PollingStation

class Command(BaseHalaroseCsvImporter):
    council_id      = 'E09000029'
    addresses_name  = 'parl.2017-06-08/Version 1/polling_station_export-2017-05-08.csv'
    stations_name   = 'parl.2017-06-08/Version 1/polling_station_export-2017-05-08.csv'
    elections       = ['parl.2017-06-08']
    csv_encoding    = 'latin-1'

    # Hounslow have supplied an additional file with
    # better grid references for the polling stations
    def post_import(self):
        filepath = os.path.join(
            self.base_folder_path,
            'parl.2017-06-08/Version 1/Sutton polling station addresses.csv'
        )
        gridrefs = self.get_data('csv', filepath)

        print("Updating grid refs...")
        for record in gridrefs:
            stations = PollingStation.objects.filter(
                council_id=self.council_id,
                internal_council_id=record.pollingstationnumber
            )
            if len(stations) == 1:
                station = stations[0]
                station.location = Point(
                    float(record.easting),
                    float(record.northing),
                    srid=27700
                )
                station.save()
            else:
                print("Could not find station id " + record.pollingstationnumber)
        print("...done")
