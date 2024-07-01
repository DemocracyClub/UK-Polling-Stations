from data_importers.base_importers import BaseCsvStationsShpDistrictsImporter
from django.contrib.gis.geos import Point


class Command(BaseCsvStationsShpDistrictsImporter):
    council_id = "DGY"
    stations_name = "2024-07-04/2024-07-01T15:29:07/DGC_Polling_Stations_June24.csv"
    districts_name = (
        "2024-07-04/2024-07-01T15:29:07/Polling_Districts_Changes_Approved.shp"
    )
    elections = ["2024-07-04"]

    def pre_import(self):
        pass

    def station_record_to_dict(self, record):
        return {
            "internal_council_id": f"{record.district_c}-{record.uprn}",
            "polling_district_id": record.district_c.strip(),
            "postcode": None,
            "address": record.polling_pl,
            "location": Point(int(record.easting), int(record.northing), srid=27700),
        }
        return super().station_record_to_dict(record)

    def district_record_to_dict(self, record):
        return {
            "internal_council_id": record["district_c"].strip(),
            "name": record["district_n"].strip(),
        }
