from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000044"
    council_name = "North Lanarkshire"
    elections = []

    def district_record_to_dict(self, record):
        # clean up codes
        record[0] = (
            self.parse_string(record[0])
            .upper()
            .replace("L00", "L")
            .replace("L0", "L")
            .strip()
        )
        return super().district_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)
        if rec:
            codes = rec["internal_council_id"].replace(" and ", ",").split(",")
            stations = []
            for code in codes:
                new_rec = {
                    "internal_council_id": code.strip().upper(),
                    "postcode": rec["postcode"],
                    "address": rec["address"],
                }
                stations.append(new_rec)
            return stations
        return rec
