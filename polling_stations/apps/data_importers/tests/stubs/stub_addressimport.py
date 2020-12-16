import os
from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseCsvStationsCsvAddressesImporter

"""
Define a stub implementation of address importer we can run tests against
"""


class Command(BaseCsvStationsCsvAddressesImporter):

    srid = 4326
    council_id = "X01000000"
    addresses_name = "addresses.csv"
    stations_name = "stations.csv"
    base_folder_path = os.path.join(
        os.path.dirname(__file__), "../fixtures/csv_importer"
    )

    def address_record_to_dict(self, record):
        return {
            "council": self.council,
            "uprn": record.uprn,
            "address": record.address,
            "postcode": record.postcode,
            "polling_station_id": record.polling_station,
        }

    def station_record_to_dict(self, record):
        location = Point(float(record.lng), float(record.lat), srid=self.get_srid())
        return {
            "council": self.council,
            "internal_council_id": record.internal_council_id,
            "postcode": record.postcode,
            "address": record.address,
            "location": location,
        }
