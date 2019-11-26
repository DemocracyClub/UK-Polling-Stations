from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000107"
    addresses_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-07.csv"
    stations_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-07.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        # These are single records listed as 'Other Electors Address'
        # no addresses are assigned. So probably don't cause problems, but
        # dropping them to squash warnings.
        if (record.pollingstationnumber, record.pollingstationname) in [
            ("63", "Hodsoll Street & Ridley Village Hall"),
            ("64", "Longfield & Hartley Scout HQ"),
            ("66", "Fawkham and Hartley Church Centre"),
        ]:
            return None
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.houseid.strip() in ["9004672", "9004673"]:
            rec["postcode"] = "DA2 7AP"

        if uprn in [
            "100060873013",  # DA28AX -> DA28DL : Beacon House Shellbank Lane, Bean, Dartford, Kent
        ]:
            rec["accept_suggestion"] = True

        return rec
