from data_collection.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "E09000017"
    addresses_name = "europarl.2019-05-23/Version 1/PropertyPostCodePollingStationWebLookup-2019-04-29.TSV"
    stations_name = "europarl.2019-05-23/Version 1/PropertyPostCodePollingStationWebLookup-2019-04-29.TSV"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn == "10092982613":
            rec["postcode"] = "UB4 0SE"

        if uprn == "100021447278":
            rec["postcode"] = "HA6 3SJ"

        if uprn == "10093736200":
            rec["postcode"] = "UB10 0TX"

        if uprn == "100023413509":
            rec["postcode"] = "UB10 8AQ"

        if uprn in [
            "10090329328",  # UB79LW -> UB49LW : 11  Adelaide House Perth Avenue
            "10092980468",  # UB33PF -> UB83PF : 9A  10A Carlton Court Bosanquet Close
            "10092982616",  # HA40SE -> UB40SE : Flat 5  366-370 Uxbridge Road
            "10092982617",  # HA40SE -> UB40SE : Flat 6  366-370 Uxbridge Road
            "10022805692",  # UB100QB -> UB100BQ : Flat 3  134 Jefferson Court Vine Lane
        ]:
            rec["accept_suggestion"] = True

        return rec
