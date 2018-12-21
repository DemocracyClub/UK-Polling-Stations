from data_collection.management.commands import BaseShpStationsShpDistrictsImporter


class Command(BaseShpStationsShpDistrictsImporter):
    srid = 27700
    council_id = "E07000037"
    districts_name = "High Peak Polling Districts"
    stations_name = "High Peak Polling Districts.shp"
    elections = [
        "local.derbyshire.2017-05-04",
        #'parl.2017-06-08'
    ]

    def district_record_to_dict(self, record):
        name = str(record[0]).strip()

        # codes are embedded in the name string: extract them
        code = name[name.find("(") + 1 : name.find(")")].strip()

        return {"internal_council_id": code, "name": name, "polling_station_id": code}

    def station_record_to_dict(self, record):
        name = str(record[0]).strip()

        # codes are embedded in the name string: extract them
        code = name[name.find("(") + 1 : name.find(")")].strip()

        return {
            "internal_council_id": code,
            "postcode": "",
            "address": str(record[1]).strip(),
            "location": None,
        }
