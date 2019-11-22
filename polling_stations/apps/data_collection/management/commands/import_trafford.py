from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000009"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019trafford.CSV"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019trafford.CSV"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = ","
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "200000333851":
            rec["postcode"] = "M41 6AS"

        if record.addressline1 == "78B High Elm Road":
            rec["postcode"] = "WA15 0HX"

        if uprn in [
            "10070405338",
            "10070405338",
            "100011646326",
            "100011693362",
            "100011622567",
            "100011679026",
        ]:
            return None

        if uprn in [
            "100012491068",  # WA144RJ -> WA145RJ : 1 Red House Cottages, Red House Lane, Dunham Massey
            "10070444322",  # WA145UX -> WA145UZ : Apartment 1, 2 Badger Road, West Timperley, Altrincham
            "10070444323",  # WA145UX -> WA145UZ : Apartment 2, 2 Badger Road, West Timperley, Altrincham
            "10070444324",  # WA145UX -> WA145UZ : Apartment 3, 2 Badger Road, West Timperley, Altrincham
            "100012495530",  # M314WJ -> M314NL : Carlton, 29 Warburton Lane, Partington
            "200000333945",  # M416JU -> M416DU : 83 Irlam Road, Flixton
            "100011674930",  # M416JS -> M416GT : 12 The Avenue, Flixton
            "100012496466",  # M337WH -> M337QH : Bridge Inn, Dane Road, Sale]
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10070460306",  # WA158UH -> WA158SZ : 3 Great Oak Drive, Altrincham
            "200000340318",  # M337RE -> M337TY : Apartment 18, 100 Washway Road, Sale
            "100011700864",  # M332UW -> M334RZ : 264 Norris Road, Sale
            "10070456948",  # 31A Ludford Grove, Sale
        ]:
            rec["accept_suggestion"] = False

        return rec
