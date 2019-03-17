from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E06000032"
    addresses_name = (
        "local.2019-05-02/Version 1/Democracy Club - Polling DistrictsLuton.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/Democracy Club - Polling StationsLuton.csv"
    )
    elections = ["local.2019-05-02"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10001038309",  # LU40HF -> LU40FH : 228 Servite Court, Morecambe Close, Luton
            "100080152018",  # LU49LQ -> LU49LF : 54 High Street, Leagrave, Luton
            "100080152011",  # LU49LQ -> LU49LF : 36 High Street, Leagrave, Luton
            "100080152012",  # LU49LQ -> LU49LF : 40 High Street, Leagrave, Luton
            "100080152013",  # LU49LQ -> LU49LF : 42 High Street, Leagrave, Luton
            "100080152015",  # LU49LQ -> LU49LF : 46 High Street, Leagrave, Luton
            "100080152016",  # LU49LQ -> LU49LF : 50 High Street, Leagrave, Luton
            "100080152017",  # LU49LQ -> LU49LF : 52 High Street, Leagrave, Luton
        ]:
            rec["accept_suggestion"] = True

        if uprn in ["100080171226"]:  # LU15HN -> LU11QZ : 49 Wilsden Avenue, Luton
            rec["accept_suggestion"] = False

        return rec
