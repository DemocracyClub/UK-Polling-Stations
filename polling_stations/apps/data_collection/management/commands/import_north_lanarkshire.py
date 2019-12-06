from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000050"
    council_name = "North Lanarkshire"
    elections = ["parl.2019-12-12"]

    def district_record_to_dict(self, record):
        # clean up codes
        record[0] = (
            self.parse_string(record[0])
            .upper()
            .replace("L00", "L")
            .replace("L0", "L")
            .strip()
        )

        # This district doesn't appear in the Notice of Situation of Polling Places
        # But does appear in source data. Throwing it away to be safe
        if record[0] == "NL43":
            return None

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
                    "address": rec["address"].replace("?", "'"),
                }

                # fixes based on comparison to the Notice of polling Place pdf
                if code == "NL51":
                    new_rec["postcode"] = "ML5 2QT"
                    new_rec["address"] = "Masonic Hall\nMain Street\nGlenboig"
                    new_rec["location"] = None

                if code == "NL45":
                    new_rec[
                        "address"
                    ] = "Skills Academy, Former Inclusion Support Base\n41 Townhead Road\nCoatbridge"
                    new_rec["location"] = None

                # Throw away coressponding station, to district which doesn't appear
                # in Notice of Situation of Polling places.
                if code == "NL43":
                    new_rec = None

                stations.append(new_rec)
            return stations
        return rec
