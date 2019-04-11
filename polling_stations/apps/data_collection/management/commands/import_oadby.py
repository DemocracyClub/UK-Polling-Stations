from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000135"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019OW.CSV"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019OW.CSV"
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100030582044",  # LE22DB -> LE25DB : 36-38 Bankart Avenue, Oadby, Leicester
            "200001140229",  # LE25AW -> LE24LZ : Flat 1 St Pauls Court, Chapel Street, Oadby, Leicester
            "200001140230",  # LE25AW -> LE24LZ : Flat 2 St Pauls Court, Chapel Street, Oadby, Leicester
            "200001140231",  # LE25AW -> LE24LZ : Flat 3 St Pauls Court, Chapel Street, Oadby, Leicester
            "200001140232",  # LE25AW -> LE24LZ : Flat 4 St Pauls Court, Chapel Street, Oadby, Leicester
            "200001140233",  # LE25AW -> LE24LZ : Flat 5 St Pauls Court, Chapel Street, Oadby, Leicester
            "10010147237",  # LE25QP -> LE182LE : 9 Honeywell Close, Oadby, Leicester
            "10010147209",  # LE183QH -> LE181DZ : 12A Waterloo Crescent, Wigston, Leicestershire
        ]:
            rec["accept_suggestion"] = False

        return rec
