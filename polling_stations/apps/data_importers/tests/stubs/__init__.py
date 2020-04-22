from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseCsvStationsJsonDistrictsImporter


class BaseStubCsvStationsJsonDistrictsImporter(BaseCsvStationsJsonDistrictsImporter):

    council_id = "X01000000"

    def district_record_to_dict(self, record):
        properties = record["properties"]
        return {
            "council": self.council,
            "internal_council_id": properties["id"],
            "name": properties["name"],
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
