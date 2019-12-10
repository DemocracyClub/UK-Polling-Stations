from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000008"
    council_name = "East Ayrshire"
    elections = ["parl.2019-12-12"]

    def station_record_to_dict(self, record):
        def duplicate_records(rec, codes, stations):
            for code in codes:
                stations.append(
                    {
                        "internal_council_id": code,
                        "postcode": rec["postcode"],
                        "address": rec["address"],
                    }
                )
            return stations

        rec = super().station_record_to_dict(record)
        if rec:
            stations = [rec]

            # Updates from SoPP review.
            if rec["internal_council_id"] == "E104":
                stations = duplicate_records(rec, ["E106", "E107"], stations)
            if rec["internal_council_id"] == "E110":
                stations = duplicate_records(rec, ["E606"], stations)
            if rec["internal_council_id"] == "E201":
                stations = duplicate_records(rec, ["E205"], stations)
            if rec["internal_council_id"] == "E203":
                stations = duplicate_records(rec, ["E204"], stations)
            if rec["internal_council_id"] == "E304":
                stations = duplicate_records(rec, ["E306"], stations)
            if rec["internal_council_id"] == "E305":
                stations = duplicate_records(rec, ["E309"], stations)
            if rec["internal_council_id"] == "E307":
                stations = duplicate_records(rec, ["E310"], stations)
            if rec["internal_council_id"] == "E313":
                stations = duplicate_records(rec, ["E401"], stations)
            if rec["internal_council_id"] == "E411":
                stations = duplicate_records(rec, ["E403", "E404", "E405"], stations)
            if rec["internal_council_id"] == "E603":
                stations = duplicate_records(rec, ["E607"], stations)
            if rec["internal_council_id"] == "E701":
                stations = duplicate_records(rec, ["E710"], stations)
            if rec["internal_council_id"] == "E704":
                stations = duplicate_records(rec, ["E807"], stations)
            if rec["internal_council_id"] == "E708":
                stations = duplicate_records(rec, ["E808"], stations)

            return stations
        return rec
