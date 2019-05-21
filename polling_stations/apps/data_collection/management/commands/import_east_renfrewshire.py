from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000011"
    council_name = "East Renfrewshire"
    elections = ["europarl.2019-05-23"]

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if not rec:
            return None

        # SpatilHub data not up-to-date.
        # Corrections from council
        if rec["internal_council_id"] == "EE14":
            return {
                "internal_council_id": rec["internal_council_id"],
                "address": "The Church Of Broom\n1 Broom Road East\nNewton Mearns\nEast Renfrewshire",
                "postcode": "G77 5HN",
                "location": None,
            }
        if rec["internal_council_id"] == "EE16":
            return {
                "internal_council_id": rec["internal_council_id"],
                "address": "Lygate House\n224 - 226 Ayr Road\nNewton Mearns\nEast Renfrewshire",
                "postcode": "G77 6FR",
                "location": None,
            }
        if rec["internal_council_id"] == "ES04":
            return {
                "internal_council_id": rec["internal_council_id"],
                "address": "St Andrews Church\n2 Ralston Road\nBarrhead\nEast Renfrewshire",
                "postcode": "G78 2RR",
                "location": None,
            }

        return rec
