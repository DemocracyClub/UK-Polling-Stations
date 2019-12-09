from data_collection.management.commands import BaseScotlandSpatialHubImporter


class Command(BaseScotlandSpatialHubImporter):
    council_id = "S12000021"
    council_name = "North Ayrshire"
    elections = ["parl.2019-12-12"]

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)
        if rec:
            codes = rec["internal_council_id"].split(",")
            stations = []
            for code in codes:
                code = code.strip()
                new_rec = {
                    "internal_council_id": code.strip(),
                    "postcode": rec["postcode"],
                    "address": rec["address"],
                }

                # fixes

                # Station with no matching district
                if code == "N608":
                    new_rec = None

                if code == "N002":
                    new_rec[
                        "address"
                    ] = "FULLARTON COMMUNITY HUB, 1 SCHOOL LANE, IRVINE, KA12 8DF"
                    new_rec["location"] = None

                if code == "N111":
                    new_rec[
                        "address"
                    ] = "NETHERMAINS COMMUNITY CENTRE, KILWINNING, KA13 6EU"
                    new_rec["location"] = None

                if code == "N302":
                    new_rec["address"] = "KILWINNING ACADEMY, DALRY ROAD, KILWINNING"
                    new_rec["location"] = None

                if code in ["N402", "N406"]:
                    new_rec[
                        "address"
                    ] = "THREE TOWNS MENS SHED, PRIMROSE PLACE, SALTCOATS"
                    new_rec["location"] = None

                if code in ["N504", "N905"]:
                    new_rec[
                        "address"
                    ] = "ST PETER'S PRIMARY SCHOOL, SOUTH ISLE ROAD, ARDROSSAN"
                    new_rec["location"] = None

                if code in ["N706", "N707"]:
                    new_rec["address"] = "BEITH PARISH CHURCH, KIRK ROAD, BEITH"
                    new_rec["location"] = None

                if code == "N702":
                    new_rec[
                        "address"
                    ] = "ST BRIDGET'S PRIMARY SCHOOL, HAGTHORN AVENUE, KILBIRNIE"
                    new_rec["location"] = None

                if code == "N902":
                    new_rec[
                        "address"
                    ] = "ST ANTHONY'S PRIMARY SCHOOL, SALTCOATS, KA21 6DE"
                    new_rec["location"] = None

                stations.append(new_rec)
            return stations
        return rec
