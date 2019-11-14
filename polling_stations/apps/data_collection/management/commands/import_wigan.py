from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000010"
    addresses_name = "parl.2019-12-12/Version 2/Democracy_Club__12December2019Wig.tsv"
    stations_name = "parl.2019-12-12/Version 2/Democracy_Club__12December2019Wig.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "200004805060":
            rec["postcode"] = "WN7 1BT"

        if uprn == "10091702455":
            rec["postcode"] = "WN6 0GU"

        if uprn == "10091700365":
            rec["postcode"] = "WN7 1LS"

        if uprn in [
            "10014065653",  # WN60TE -> WN60UL : 57 Granny Flat School Lane
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
            "200001924721",  # WN40JH -> WN40JA : High Brooks Stables High Brooks
            "100012500742",  # WN24XR -> WN24XS : The Old Barn Smiths Lane
            "100011798794",  # WN59DL -> WN59DN : Flat Above  301-305 Ormskirk Road
        ]:
            rec["accept_suggestion"] = False

        # 17 Chester Street, Leigh WN7 2LS. NB addressbase UPRN is "10091700365"
        if uprn == "100011763908":
            rec["postcode"] = "WN71LS"

        return rec
