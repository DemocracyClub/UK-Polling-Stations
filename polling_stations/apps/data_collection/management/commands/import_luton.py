from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E06000032"
    addresses_name = "parl.maybe/Version 1/luton-DC - Polling Districts.csv"
    stations_name = "parl.maybe/Version 1/luton-DC - Polling Stations.csv"
    elections = ["parl.maybe"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "10001037360":
            rec["postcode"] = "LU2 7QG"
            rec["accept_suggestion"] = False

        if uprn in [
            "10001038309",  # LU40HF -> LU40FH : 228 Servite Court, Morecambe Close, Luton
            "200003273279",  # LU31TL -> LU27AU : SCHOOL HOUSE BARNFIELD COLLEGE, BARNFIELD AVENUE, LUTON
            "100080152039",  # LU49LQ -> LU49LJ : 130 HIGH STREET, LUTON
        ]:
            rec["accept_suggestion"] = True

        if uprn in ["100080171226"]:  # LU15HN -> LU11QZ : 49 Wilsden Avenue, Luton
            rec["accept_suggestion"] = False

        return rec
