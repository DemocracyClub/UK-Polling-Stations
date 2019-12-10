from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000039"
    council_name = "West Dunbartonshire"
    elections = ["parl.2019-12-12"]

    def station_record_to_dict(self, record):

        # Corrections based on checking notice of polling place
        addresses = {
            "LE8D": "DALMONACH MOBILE POLLING PLACE, FIRST AVENUE, BONHILL, G83 9AU",
            "DU13D": "WESTBRIDGEND MOBILE POLLING PLACE, WESTBRIDGEND, DUMBARTON, G82 4BJ",
            "CC5C": "OUR LADY OF LORETTO PRIMARY SCHOOL, CASTLE SQUARE, CASTLE STREET, DALMUIR, CLYDEBANK, G81 4HN",
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
