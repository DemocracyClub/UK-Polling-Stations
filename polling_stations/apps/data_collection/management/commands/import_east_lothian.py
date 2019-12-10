from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000010"
    council_name = "East Lothian"
    elections = ["parl.2019-12-12"]

    def station_record_to_dict(self, record):

        # Corrections based on checking notice of polling place
        addresses = {
            "EL3A": "TRANENT TOWN HALL, CHURCH STREET, TRANENT",
            "EL5E": "ATHELSTANEFORD VILLAGE HALL, MAIN STREET, ATHELSTANEFORD",
            "EL5F": "MORHAM VILLAGE HALL, MORHAM",
            "EL4D": "FENTON BARNS MAIN OFFICE, FENTON BARNS DIRLETON NORTH BERWICK EH39 5BW",
            "EL4F": "ST MARYS CHURCH HALL, WHITEKIRK NORTH BERWICK DUNBAR",
            "EL6I": "OLDHAMSTOCKS VILLAGE HALL, OLDHAMSTOCKS INNERWICK COCKBURNSPATH TD13 5XN",
        }

        rec = super().station_record_to_dict(record)

        if rec:
            try:
                rec["address"] = addresses[rec["internal_council_id"]]
                rec["location"] = None
                return rec
            except KeyError:
                return rec

        return rec
