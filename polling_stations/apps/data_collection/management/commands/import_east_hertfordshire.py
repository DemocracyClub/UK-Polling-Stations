from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000242"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019E Herts.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019E Herts.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10033104592":
            rec["postcode"] = "CM20 2QP"

        if uprn == "10023088041":
            rec["postcode"] = "CM20 2FP"

        if uprn == "10023090475":
            return None

        if uprn in [
            "100080727137",  # CM233QY -> CM235QY : 34 Shortcroft, Bishops Stortford, Herts
            "100081117602",  # CM232JH -> CM232JJ : Wintersett, 5 Whitehall Lane, Bishops Stortford, Herts
            "10033096663",  # SG90HH -> SG90EA : Bentleys, Hare Street, Herts
            "10033104823",  # SG141LR -> SG142PX : Rose Cottage, Goldings Lane, Hertford, Herts
            "10034515257",  # CM210HH -> CM210DB : 1 Highfield, Crofters, Sawbridgeworth, Herts
            "10034515290",  # CM210HX -> CM210DB : 36 Highfield, Crofters, Sawbridgeworth, Herts
            "10034515291",  # CM210BD -> CM210DB : 37 Highfield, Crofters, Sawbridgeworth, Herts
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100080722649",  # CM232QT -> CM232QY : 70 Hadham Road, Bishops Stortford, Herts
            "100081118102",  # SG90DX -> SG90DY : The Small Barn, Hare Street, Herts
            "100080736259",  # SG142LB -> SG142LG : The Hill, 236/238 Hertingfordbury Road, Hertford, Herts
            "10034620003",  # SG142NE -> SG142NA : The Lodge, Marden Hill, Hertford, Herts, Herts
            "100081121082",  # SG111PW -> SG111PJ : Tregarron, Standon Hill, Ware, Herts
            "10033105203",  # SG111EZ -> SG111HA : The Gables, Old Hall Green, Standon, Herts
            "10033095127",  # SG143NE -> SG143NQ : The Beehive Cottage, Woodhall Park, Watton At Stone, Herts
            "10033095128",  # SG143NE -> SG143NQ : The Garden House, Woodhall Park, Watton At Stone, Herts
            "100081120184",  # SG111NW -> SG111NY : Bromley Hall, Bromley Lane, Standon, Herts
        ]:
            rec["accept_suggestion"] = False

        return rec
