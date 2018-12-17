"""
Import COUNCIL
"""
import sys

from django.contrib.gis.geos import Point

from data_collection.management.commands import BaseCsvStationsJsonDistrictsImporter


class Command(BaseCsvStationsJsonDistrictsImporter):
    """
    Imports the Polling Station data from COUNCIL
    """

    council_id = "COUNCIL_ID"
    districts_name = "DISTRICT_FILE.geojson"
    stations_name = "STATION_FILE.csv"
    """
    if geojson uses lat/long co-ordinates, set districts_srid = 4326
    if geojson uses UK national grid, remove this
    """
    districts_srid = 4326
    """
    List of Election IDs the data imported by this script relates to
    https://democracyclub.org.uk/projects/election-ids/
    """
    elections = []

    def district_record_to_dict(self, record):
        properties = record["properties"]

        print("District:", properties)
        sys.exit(1)

        return {
            "council": self.council,
            "internal_council_id": properties["id"],
            "name": properties["name"],
        }

    def station_record_to_dict(self, record):
        print("Station: ", record)
        sys.exit(1)

        try:
            location = Point(
                int(record.easting), int(record.northing), srid=self.get_srid()
            )
        except ValueError:
            location = Point(
                float(record.easting), float(record.northing), srid=self.get_srid()
            )
        return {
            "internal_council_id": record.internal_id,
            "postcode": record.address.split(",")[-1],
            "address": "\n".join(record.address.split(",")[:-1]),
            "location": location,
        }
