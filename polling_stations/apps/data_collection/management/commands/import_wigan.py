from data_collection.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "E08000010"
    addresses_name = "local.2019-05-02/Version 1/PropertyPostCodePollingStationWebLookup-2019-03-26.TSV"
    stations_name = "local.2019-05-02/Version 1/PropertyPostCodePollingStationWebLookup-2019-03-26.TSV"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # these co-ordinates were a missing a digit
        if record.pollingplaceid == "4905":
            record = record._replace(pollingplaceeasting="371720")
        if record.pollingplaceid == "4957":
            record = record._replace(pollingplaceeasting="356840")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "200004805060":
            rec["postcode"] = "WN7 1BT"

        if uprn == "10091702455":
            rec["postcode"] = "WN6 0GU"

        if uprn in [
            "10014065653",  # WN60TE -> WN60UL : 57 Granny Flat School Lane
            "200004801589",  # WN67NZ -> WN67LZ : Flat Over  132 Woodhouse Lane
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10014060608",  # WN25TA -> WN25NY : 10 Caravan Site
            "10014060609",  # WN25TA -> WN25NY : 11 Caravan Site
            "10014060610",  # WN25TA -> WN25NY : 12 Caravan Site
            "10014060611",  # WN25TA -> WN25NY : 13 Caravan Site
            "10014060612",  # WN25TA -> WN25NY : 14 Caravan Site
            "10014060613",  # WN25TA -> WN25NY : 15 Caravan Site
            "10014060614",  # WN25TA -> WN25NY : 16 Caravan Site
            "100012497983",  # WN73SE -> WN73SD : Bowland Field Farm Grave Oak Lane
            "200001924721",  # WN40JH -> WN40JA : High Brooks Stables High Brooks
            "100012500742",  # WN24XR -> WN24XS : The Old Barn Smiths Lane
            "100012499758",  # WN50LL -> WN58QE : 375 Green Gables Gathurst Road
            "100011798794",  # WN59DL -> WN59DN : Flat Above  301-305 Ormskirk Road
        ]:
            rec["accept_suggestion"] = False

        return rec
