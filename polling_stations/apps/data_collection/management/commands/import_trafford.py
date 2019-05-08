from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000009"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Trafford.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Trafford.tsv"
    elections = ["local.2019-05-02", "europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "200000333851":
            rec["postcode"] = "M41 6AS"

        if uprn == "10070456948":
            rec["accept_suggestion"] = False

        if uprn in [
            "100012491068",  # WA144RJ -> WA145RJ : 1 Red House Cottages, Red House Lane, Dunham Massey
            "10070444322",  # WA145UX -> WA145UZ : Apartment 1, 2 Badger Road, West Timperley, Altrincham
            "10070444323",  # WA145UX -> WA145UZ : Apartment 2, 2 Badger Road, West Timperley, Altrincham
            "10070444324",  # WA145UX -> WA145UZ : Apartment 3, 2 Badger Road, West Timperley, Altrincham
            "100012495530",  # M314WJ -> M314NL : Carlton, 29 Warburton Lane, Partington
            "200000333945",  # M416JU -> M416DU : 83 Irlam Road, Flixton
            "100011674930",  # M416JS -> M416GT : 12 The Avenue, Flixton
            "100012496466",  # M337WH -> M337QH : Bridge Inn, Dane Road, Sale
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10070460306",  # WA158UH -> WA158SZ : 3 Great Oak Drive, Altrincham
            "200000340318",  # M337RE -> M337TY : Apartment 18, 100 Washway Road, Sale
            "100012491343",  # WA143HD -> WA143HF : Woodhatch, South Downs Road, Bowdon
            "100011654153",  # M417DQ -> M417DN : 50 Davyhulme Road, Davyhulme
            "100011700864",  # M332UW -> M334RZ : 264 Norris Road, Sale
        ]:
            rec["accept_suggestion"] = False

        return rec
