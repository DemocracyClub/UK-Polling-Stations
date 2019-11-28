from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000103"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-08watford.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-08watford.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in ["100080947255", "100080947259"]:
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "WD18 7JT"
            return rec

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # These are single records listed as 'Other Electors Address'
        # no addresses are assigned. So probably don't cause problems, but
        # dropping them to squash warnings.
        if (record.pollingstationnumber, record.pollingstationname) in [
            ("61", "Manor House Sports & Social Centre"),
            ("62", "Scout Hut"),
            ("63", "Tanners Wood Hall"),
            ("65", "YMCA Woodlands Centre"),
            ("67", "Coates Way JMI and Nursery School"),
            ("69", "Oxhey Hall Community Association Hall"),
            ("68", "Leavesden Green Infants Hall"),
        ]:
            return None
        return super().station_record_to_dict(record)
