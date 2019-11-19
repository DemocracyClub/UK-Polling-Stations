import os
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseHalaroseCsvImporter
from pollingstations.models import PollingStation


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000174"
    addresses_name = "parl.2019-12-12/Version 2/polling_station_export-2019-11-12.csv"
    stations_name = "parl.2019-12-12/Version 2/polling_station_export-2019-11-12.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def get_station_hash(self, record):
        return "-".join([record.pollingstationnumber.strip(),])

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "10091484857":
            rec["postcode"] = "NG19 7NH"

        return rec

    def post_import(self):
        filepath = os.path.join(
            self.base_folder_path, "parl.2019-12-12/Version 2/Polling Station.csv"
        )
        gridrefs = self.get_data("csv", filepath)

        print("Updating grid refs...")
        for record in gridrefs:
            stations = PollingStation.objects.filter(
                council_id=self.council_id,
                internal_council_id="-".join([record.number.strip()]),
            )
            if len(stations) == 1:
                station = stations[0]
                station.location = Point(
                    float(record.origin_x), float(record.origin_y), srid=27700
                )
                self.check_station_point(
                    {"location": station.location, "council_id": station.council_id,}
                )
                station.save()
            else:
                print("Could not find station id " + "-".join([record.number.strip()]))
        print("...done")
