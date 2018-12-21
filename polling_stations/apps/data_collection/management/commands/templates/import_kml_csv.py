"""
Import COUNCIL
"""
import sys

from django.contrib.gis.geos import Point, GEOSGeometry

from data_collection.management.commands import BaseCsvStationsKmlDistrictsImporter


class Command(BaseCsvStationsKmlDistrictsImporter):
    """
    Imports the Polling Station data from COUNCIL
    """

    council_id = "COUNCIL_ID"
    districts_name = "DISTRICT_FILE.kmz"
    stations_name = "STATION_FILE.csv"
    """
    List of Election IDs the data imported by this script relates to
    https://democracyclub.org.uk/projects/election-ids/
    """
    elections = []

    # we must always implement station_record_to_dict()
    def station_record_to_dict(self, record):
        print("Station: ", record)
        sys.exit(1)

        try:
            location = Point(
                int(record.point_x), int(record.point_y), srid=self.get_srid()
            )
        except ValueError:
            location = Point(
                float(record.point_x), float(record.point_y), srid=self.get_srid()
            )
        return {
            "internal_council_id": record.polling_di,
            "postcode": "(no postcode)",
            "address": "\n".join([record.building, record.road, record.town_villa]),
            "location": location,
        }

    # sometimes it may also be necessary to override district_record_to_dict()
    def district_record_to_dict(self, record):
        print("District: ", record)
        sys.exit(1)

        geojson = self.strip_z_values(record.geom.geojson)
        poly = self.clean_poly(GEOSGeometry(geojson, srid=self.get_srid("districts")))
        return {
            "internal_council_id": record["Name"].value,
            "name": record["Name"].value,
            "area": poly,
        }
