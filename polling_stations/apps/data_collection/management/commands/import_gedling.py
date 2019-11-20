from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000173"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019gedling.tsv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019gedling.tsv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 in ("NG5 8PQ", "NG4 4PS"):
            # Unexpected polling stations for one or more properties. Removing just those properties might give
            # misleading results for the postcode if the polling station was correct.
            return None

        if uprn in [
            "10035282319",
            "100032276046",
            "100032123022",
            "100031353751",
        ]:
            return None

        if record.addressline1 == "328A Carlton Hill":
            return None

        if uprn in [
            "10035281242",  # NG35TQ -> NG35QQ : Flat 2 840 Woodborough Road, Mapperley, Nottinghamshire
            "10035281241",  # NG35TQ -> NG35QQ : Flat 1 840 Woodborough Road, Mapperley, Nottinghamshire
            "10035281243",  # NG35TQ -> NG35QQ : Flat 3 840 Woodborough Road, Mapperley, Nottinghamshire
            "10035281244",  # NG35TQ -> NG35QQ : Flat 4 840 Woodborough Road, Mapperley, Nottinghamshire
            "10035281246",  # NG35TQ -> NG35QQ : Flat 5 840 Woodborough Road, Mapperley, Nottinghamshire
            "10035281247",  # NG35TQ -> NG35QQ : Flat 6 840 Woodborough Road, Mapperley, Nottinghamshire
            "100031358592",  # NG41LX -> NG41LZ : 64 Ernest Road, Carlton, Nottinghamshire
            "100032100963",  # NG158GD -> NG159HP : The Gatehouse Lodge, Newstead, Nottinghamshire
            "10002888179",  # NG158GD -> NG158GE : Mount Charlotte, Newstead Abbey Park, Ravenshead, Nottinghamshire
            "100031366279",  # NG36BN -> NG36BS : 106 Kent Road, Mapperley, Nottinghamshire
            "100031366280",  # NG36BN -> NG36BS : 108 Kent Road, Mapperley, Nottinghamshire
            "100031360828",  # NG57BN -> NG57BP : Ernehale Lodge Nursing Home, Furlong Street, Arnold, Nottinghamshire
            "100031370521",  # NG58PB -> NG58PE : Wernbank Cottage, Mansfield Road, Bestwood, Nottinghamshire
            "10002896029",  # NG36HE -> NG36HG : Flat above The Punchbowl, 214 Porchester Road, Mapperley, Nottingham
        ]:
            rec["accept_suggestion"] = True
        #
        if uprn in [
            "200001152310",  # NG44FL -> NG44FG : 267A Westdale Lane East, Carlton, Nottinghamshire
            "200001152316",  # NG44FN -> NG44FG : 273A Westdale Lane East, Carlton, Nottinghamshire
            "10002892754",  # NG44FL -> NG44FG : 275A Westdale Lane East, Carlton, Nottinghamshire
            "200001152115",  # NG43JW -> NG43JU : 69 Westdale Lane East, Carlton, Nottinghamshire
            "200001152117",  # NG43JW -> NG43JU : 71 Westdale Lane East, Carlton, Nottinghamshire
            "200001152308",  # NG44FN -> NG44FW : 266A Westdale Lane East, Gedling, Nottinghamshire
            "200001152313",  # NG44FN -> NG44FW : 270 Westdale Lane East, Gedling, Nottinghamshire
            "200001152312",  # NG44FN -> NG44FW : 270A Westdale Lane East, Gedling, Nottinghamshire
            "200001152248",  # NG44FN -> NG44FT : 202 Westdale Lane East, Carlton, Nottinghamshire
            "100031346832",  # NG146EF -> NG146EE : Woodborough Hall, Bank Hill, Woodborough, Nottinghamshire
            "100031347797",  # NG58NE -> NG58HT : Beauclark House, Bestwood Lodge Drive, Bestwood, Nottinghamshire
            "100031359284",  # NG146JZ -> NG146LN : Oxgang, Flatts Lane, Calverton, Nottinghamshire
            "100032099652",  # NG146FG -> NG146FN : The Flat Oscar`s Lounge & Restaurant,, Main Street, Calverton, Nottinghamshire
            "100031348280",  # NG146FR -> NG146ED : The Poplars, Bonner Hill, Calverton, Nottinghamshire
            "10002896692",  # NG58PJ -> NG158FJ : Miller and Carter Steakhouse, Mansfield Road, Arnold, Nottingham
            "10035287615",  # NG158JU -> NG44LU : 31 Askew Road, Linby, Nottinghamshire
        ]:
            rec["accept_suggestion"] = False

        if record.addressline6 in ["NG3 6DS", "NG4 3DQ"]:
            rec["accept_suggestion"] = False

        return rec
