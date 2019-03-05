from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E06000016"
    addresses_name = "local.2019-05-02/Version 1/Democracy Club LCC Polling Places List 2 May 2019.csv"
    stations_name = "local.2019-05-02/Version 1/Democracy Club LCC Polling Places List 2 May 2019.csv"
    elections = ["local.2019-05-02"]

    station_postcode_search_fields = [
        "polling_place_postcode",
        "polling_place_address_2",
    ]
    station_address_fields = ["polling_place_name", "polling_place_address_1"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if len(record.addressline6) <= 6:
            return None

        if record.addressline6 == "LE3 3AT":
            rec["postcode"] = "LE1 3AT"

        if uprn in ["2465203014", "2465203012", "2465203013"]:
            rec["postcode"] = "LE1 5TE"

        if uprn in [
            "2465188649",  # LE16NB -> LE16EY : First Floor Flat 108 Y.M.C.A., 7 East Street, Leicester
            "2465188810",  # LE16NB -> LE16EY : Third Floor Cluster Flat 3, Room 311-314 Y.M.C.A., 7 East Street, Leicester
            "2465188643",  # LE16NB -> LE16EY : First Floor Flat 102 Y.M.C.A., 7 East Street, Leicester
            "2465188809",  # LE16NB -> LE16EY : Third Floor cluster Flat 2, Room 307-310 Y.M.C.A., 7 East Street, Leicester
            "2465188807",  # LE16NB -> LE16EY : Second Floor Flat 217 Y.M.C.A., 7 East Street, Leicester
            "2465188808",  # LE16NB -> LE16EY : Third Floor Cluster Flat 1, Room 301-306 Y.M.C.A., 7 East Street, Leicester
            "2465188806",  # LE16NB -> LE16EY : Second Floor Flat 216 Y.M.C.A., 7 East Street, Leicester
            "2465188645",  # LE16NB -> LE16EY : First Floor Flat 104 Y.M.C.A., 7 East Street, Leicester
            "2465188646",  # LE16NB -> LE16EY : First Floor Flat 105 Y.M.C.A., 7 East Street, Leicester
            "2465188642",  # LE16NB -> LE16EY : First Floor Flat 101 Y.M.C.A., 7 East Street, Leicester
            "2465188647",  # LE16NB -> LE16EY : First Floor Flat 106 Y.M.C.A., 7 East Street, Leicester
            "2465188813",  # LE16NB -> LE16EY : Third Floor Flat 316 Y.M.C.A., 7 East Street, Leicester
            "2465188648",  # LE16NB -> LE16EY : First Floor Flat 107 Y.M.C.A., 7 East Street, Leicester
            "2465188803",  # LE16NB -> LE16EY : Second Floor Cluster Flat 6 Room 207-210 Y.M.C.A., 7 East Street, Leicester
            "2465188644",  # LE16NB -> LE16EY : First Floor Flat 103 Y.M.C.A., 7 East Street, Leicester
            "2465188802",  # LE16NB -> LE16EY : Second Floor Cluster Flat 5 Room 201-206 Y.M.C.A., 7 East Street, Leicester
            "2465188812",  # LE16NB -> LE16EY : Third Floor Flat 315 Y.M.C.A., 7 East Street, Leicester
            "2465188811",  # LE16NB -> LE16EY : Third Floor Cluster Flat 4, Rooms 317-320 Y.M.C.A., 7 East Street, Leicester
            "2465156194",  # LE21DB -> LE21DA : The Flat, 34 St Peters Road, Leicester
            "2465184336",  # LE21DF -> LE21DB : Second Floor Flat 3, 38 St Peters Road, Leicester
            "2465184335",  # LE21DF -> LE21DB : First Floor Flat 2, 38 St Peters Road, Leicester
            "2465184334",  # LE21DF -> LE21DB : Ground Floor Flat 1, 38 St Peters Road, Leicester
            "2465179600",  # LE21DF -> LE21DB : 40 St Peters Road, Leicester
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "2465161850",  # LE54HH -> LE54HG : 337 St Saviours Road, Leicester
            "2465100401",  # LE20GU -> LE20GH : 63 Melbourne Road, Leicester
            "2465167645",  # LE46PN -> LE46QJ : The Flat, 43 Melton Road, Leicester
        ]:
            rec["accept_suggestion"] = False

        if uprn in ["2465164584", "2465164583", "2465164582"]:
            rec["accept_suggestion"] = False

        if (
            record.addressline1
            in [
                "Second Floor Cluster Flat 7 Room 212-215 Y.M.C.A.",
                "Second Floor Cluster Flat 8, Room 218-221 Y.M.C.A.",
            ]
            and record.addressline6 == "LE1 6NB"
        ):
            rec["postcode"] = "LE1 6EY"

        return rec
