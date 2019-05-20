from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "W06000011"
    addresses_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-05-08swan.csv"
    )
    stations_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-05-08swan.csv"
    )
    elections = ["europarl.2019-05-23"]
    csv_encoding = "latin-1"

    def station_record_to_dict(self, record):
        if record.pollingstationaddress_5 == "mail@clydach.wales":
            record = record._replace(pollingstationaddress_5="")

        rec = super().station_record_to_dict(record)

        if rec and rec["internal_council_id"] == "77-trinity-chapel-vestry":
            rec["location"] = None

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        # most of these UPRNs are junk
        if rec and "E" in uprn:
            rec["uprn"] = ""

        if record.pollingstationnumber == "n/a":
            return None

        if uprn == "10010042652":
            rec["postcode"] = "SA6 5PG"
        if uprn == "10010040619":
            rec["postcode"] = "SA2 0PN"
        if uprn == "10010046633":
            rec["postcode"] = "SA2 0LR"
        if uprn == "10010040846":
            rec["postcode"] = "SA1 4JP"
        if uprn == "10010037730":
            rec["postcode"] = "SA2 0NH"

        if record.housepostcode == "SA2 OSF":
            rec["postcode"] = "SA2 0SF"

        if record.housepostcode == "SA4 0FT":
            return None

        if record.houseid == "2000068":
            rec["postcode"] = "SA6 7JY"

        if record.houseid == "2100040":
            rec["postcode"] = "SA1 7JA"

        if uprn in ["10010062487", "10010062488"]:
            rec["accept_suggestion"] = False

        return rec
