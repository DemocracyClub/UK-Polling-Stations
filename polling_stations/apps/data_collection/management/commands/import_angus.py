from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000041"
    council_name = "Angus"
    elections = [
        "local.angus.2017-05-04",
        #'parl.2017-06-08'
    ]
    """
    In the Angus data, station names are in the districts file but the
    address is in the stations file, so we need to grab the station name
    when we import the district polygons and store them so we can grab
    them later when we import the station points
    """
    station_addresses = {}

    def district_record_to_dict(self, record):
        self.station_addresses[str(record[0]).strip()] = str(record[2]).strip()
        return super().district_record_to_dict(record)

    def station_record_to_dict(self, record):
        council_name = str(record[3]).strip()
        if council_name != self.council_name:
            return None

        code = str(record[1]).strip()
        if not code:
            return None

        address = "\n".join([self.station_addresses[code], str(record[0]).strip()])

        return {"internal_council_id": code, "postcode": "", "address": address}
